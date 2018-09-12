#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from datetime import timedelta
from flask import render_template, session, redirect, url_for, flash, abort, request, jsonify
from . import engineer
from .forms import SetForm, InfoForm, OperationForm, HistoryForm
from .. import db
from ..models import SetPoint, NewData, FaultList, aftercheck_list, Diagnosis, OperationRecord


def time_transform(count):
    seconds = count * 5
    if seconds >= 60:
        mins = seconds // 60
        seconds = seconds - mins * 60
        if mins >= 60:
            hours = mins // 60
            mins = mins - hours * 60
            if hours >= 24:
                days = hours // 24
                hours = hours - days * 24
                if days >= 365:
                    years = days // 365
                    days = days - years * 365
                    str_result = str(int(years)) + '年' + str(int(days)) + '天' + str(int(hours)) + '小时' + str(int(mins)) + '分' + str(int(seconds)) + '秒'
                    return str_result
                else:
                    str_result = str(int(days)) + '天' + str(int(hours)) + '小时' + str(int(mins)) + '分' + str(int(seconds)) + '秒'
                    return str_result
            else:
                str_result = str(int(hours)) + '小时' + str(int(mins)) + '分' + str(int(seconds)) + '秒'
                return str_result
        else:
            str_result = str(int(mins)) + '分' + str(int(seconds)) + '秒'
            return str_result
    else:
        str_result = str(int(seconds)) + '秒'
        return str_result


def codeToMes(code):
    if code == 1:
        return '信号丢失故障'
    elif code == 3:
        return '瞬时过流故障'
    elif code == 2:
        return '瞬时受力报警'
    elif code == 4:
        return '超出量程故障'
    elif code == 5:
        return '偏载报警'


@engineer.route('/setpoint', methods=['POST', 'GET'])
def setpoint():
    form = SetForm()
    form1 = InfoForm()
    return render_template('Setpoint.html', form=form, form1=form1)


@engineer.route('/faultreport', methods=['POST', 'GET'])
def faultreport():
    dic = {}
    dic['id'] = []
    dic['fault_time'] = []
    dic['recover_time'] = []
    dic['period_second'] = []
    dic['fault_reason'] = []
    dic['fault_state'] = []
    dic['fault_level'] = []
    data = FaultList.query.all()
    for item in data:
        dic['id'].append(item.ID)
        dic['fault_time'].append(item.FaultTime.strftime('%Y-%m-%d %H:%M:%S'))
        if item.RecoverTime:
            dic['recover_time'].append(item.RecoverTime.strftime('%Y-%m-%d %H:%M:%S'))
            dic['period_second'].append(time_transform(item.PeriodSecond / 5))
        else:
            dic['recover_time'].append('——')
            dic['period_second'].append('——')
        if item.FaultSencer:
            dic['fault_reason'].append(item.FaultSencer + ':' + codeToMes(item.FaultCode))
        # else:
        #     dic['fault_reason'].append(codeToMes(item.fault_code))
        dic['fault_state'].append('已修复' if item.FaultState == 0 else '未修复')
        dic['fault_level'].append(2 if item.FaultCode in [1, 3, 4] else 1)
    Num = len(dic['id'])
    return render_template('FaultReport.html', dic=dic, Num=Num)


@engineer.route('/operaterecord', methods=['POST', 'GET'])
def operaterecord():
    form = OperationForm()
    return render_template('OperationRecord.html', form=form)


@engineer.route('/history', methods=['POST', 'GET'])
def history():
    form = HistoryForm()
    return render_template('History.html', form=form)


@engineer.route('/insertSetpoint', methods=['POST', 'GET'])
def insertSetpoint():
    Num = int(request.form.get("Num", "0"))
    Temp = float(request.form.get("Temp", "0.0"))
    Wet = float(request.form.get("Wet", "0.0"))
    ExcV = float(request.form.get("ExcV", "0.0"))
    Sensitivity = float(request.form.get("Sensitivity", "0.0"))
    Resistance = int(request.form.get("Resistance", "0"))
    noload_set = request.form.get("noLoad", "")
    emptyload_set = request.form.get("emptyLoad", "")
    Name = request.form.get("Name", "")
    supplier = request.form.get("supplier", "")
    eqpName = request.form.get("eqpname", "")
    p = SetPoint(SencerNum=Num, Temp=Temp, Wet=Wet, ExcV=ExcV, Sensitivity=Sensitivity,
                  Resistance=Resistance, NoLoad_set=noload_set, SencerName=Name,
                  EmptyLoad_set=emptyload_set, EqpNum=eqpName, Supplier=supplier)
    db.session.add(p)
    db.session.commit()
    dic = {'success': 1}
    return jsonify(dic)


@engineer.route('/faultQuery', methods=['POST', 'GET'])
def faultQuery():
    dic = {}
    dic['axisData'] = []
    dic['Tag1'] = []
    dic['Tag2'] = []
    dic['Tag3'] = []
    dic['Tag4'] = []
    startTime = request.form.get("startTime", "")
    endTime = request.form.get("endTime", "")
    startTime = datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S") - timedelta(hours=1)
    if endTime == 'noEnd':
        result = NewData.query.filter(NewData.Timestamp > startTime).all()
    else:
        endTime = datetime.strptime(endTime, "%Y-%m-%d %H:%M:%S") + timedelta(hours=1)
        result = NewData.query.filter(NewData.Timestamp > startTime, NewData.Timestamp < endTime).all()
    for item in result:
        dic['axisData'].append(getattr(item, 'Timestamp').strftime('%Y-%m-%d %H:%M:%S'))
        dic['Tag1'].append(getattr(item, 'WeightTag1'))
        dic['Tag2'].append(getattr(item, 'WeightTag2'))
        dic['Tag3'].append(getattr(item, 'WeightTag3'))
        dic['Tag4'].append(getattr(item, 'WeightTag4'))
    return jsonify(dic)


@engineer.route('/insertOperation', methods=['POST', 'GET'])
def insertOperation():
    date = request.form.get("date", "0")
    operate = request.form.get("operate", "0.0")
    stadnard = float(request.form.get("stadnard", "0.0"))
    zero = float(request.form.get("zero", "0.0"))
    date = datetime.strptime(date, "%Y-%m-%d %H:%M")
    p = OperationRecord(record=operate, standard=stadnard, zeropoint=zero)
    db.session.add(p)
    db.session.commit()
    dic = {'success': 1}
    return jsonify(dic)


@engineer.route('/operationQuery', methods=['POST', 'GET'])
def operationQuery():
    dic = {}
    dic['Timestamp'] = []
    dic['record'] = []
    dic['standard'] = []
    dic['zeropoint'] = []
    startTime = request.form.get("startTime", "")
    endTime = request.form.get("endTime", "")
    startTime = datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S") - timedelta(hours=1)
    if endTime == 'noEnd':
        result = OperationRecord.query.filter(OperationRecord.Timestamp > startTime).all()
    else:
        endTime = datetime.strptime(endTime, "%Y-%m-%d %H:%M:%S") + timedelta(hours=1)
        result = OperationRecord.query.filter(OperationRecord.Timestamp > startTime, OperationRecord.Timestamp < endTime).all()
    for item in result:
        for key in dic.keys():
            if key == 'Timestamp':
                dic[key].append(getattr(item, key).strftime('%Y-%m-%d %H:%M:%S'))
            else:
                dic[key].append(getattr(item, key))
    return jsonify(dic)
