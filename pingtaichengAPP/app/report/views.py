#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from flask import render_template, session, redirect, url_for, flash, abort, request, jsonify
from . import report
from .forms import Queryform, Titleform
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


@report.route('/details', methods=['POST', 'GET'])
def details():
    form = Queryform()
    form1 = Titleform() 
    return render_template('Details.html', form=form, form1=form1)


@report.route('/infoQuery', methods=['POST', 'GET'])
def infoQuery():
    dic = {}
    eqp = request.form.get("eqp", "0")
    result = SetPoint.query.filter(SetPoint.EqpNum == eqp).first()
    if result:
        dic['Supplier'] = result.Supplier
        dic['SencerName'] = result.SencerName
        dic['Noload'] = result.NoLoad_set
        dic['Emptyload'] = result.EmptyLoad_set
        dic['ExcV'] = result.ExcV
        dic['Sen'] = result.Sensitivity
    else:
        dic['fail'] = 1
    return jsonify(dic)


@report.route('/pieDataQuery', methods=['POST', 'GET'])
def pieDataQuery():
    dic = {}
    startTime = request.form.get("startTime", "")
    endTime = request.form.get("endTime", "")
    startTime = datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S")
    if endTime == 'noEnd':
        fault_num = aftercheck_list.query.filter(aftercheck_list.state_fault == 1, aftercheck_list.Timestamp > startTime).count()
        alarm_num = aftercheck_list.query.filter(aftercheck_list.state_prealarm == 1, aftercheck_list.Timestamp > startTime).count()
        normal_num = aftercheck_list.query.filter(aftercheck_list.state_normal == 1, aftercheck_list.Timestamp > startTime).count()
    else:
        endTime = datetime.strptime(endTime, "%Y-%m-%d %H:%M:%S")
        fault_num = aftercheck_list.query.filter(aftercheck_list.state_fault == 1, aftercheck_list.Timestamp > startTime, aftercheck_list.Timestamp < endTime).count()
        alarm_num = aftercheck_list.query.filter(aftercheck_list.state_prealarm == 1, aftercheck_list.Timestamp > startTime, aftercheck_list.Timestamp < endTime).count()
        normal_num = aftercheck_list.query.filter(aftercheck_list.state_normal == 1, aftercheck_list.Timestamp > startTime, aftercheck_list.Timestamp < endTime).count()
    dic['fault'] = fault_num
    dic['alarm'] = alarm_num
    dic['normal'] = normal_num
    return jsonify(dic)


@report.route('/trendQuery', methods=['POST', 'GET'])
def trendQuery():
    dic = {}
    dic['standard'] = []
    dic['zero'] = []
    dic['axisData'] = []
    startTime = request.form.get("startTime", "")
    endTime = request.form.get("endTime", "")
    startTime = datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S")
    if endTime == 'noEnd':
        result = OperationRecord.query.filter(OperationRecord.Timestamp > startTime).all()
    else:
        endTime = datetime.strptime(endTime, "%Y-%m-%d %H:%M:%S")
        result = OperationRecord.query.filter(OperationRecord.Timestamp > startTime, OperationRecord.Timestamp < endTime).all()
    for item in result:
        dic['axisData'].append(getattr(item, 'Timestamp').strftime('%Y-%m-%d %H:%M:%S'))
        dic['standard'].append(getattr(item, 'standard'))
        dic['zero'].append(getattr(item, 'zeropoint'))
    return jsonify(dic)


@report.route('/faultTable', methods=['POST', 'GET'])
def faultTable():
    dic = {}
    dic['fault_time'] = []
    dic['recover_time'] = []
    dic['period_second'] = []
    dic['fault_reason'] = []
    dic['fault_state'] = []
    dic['fault_level'] = []
    startTime = request.form.get("startTime", "")
    endTime = request.form.get("endTime", "")
    startTime = datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S")
    if endTime == 'noEnd':
        result = FaultList.query.filter(FaultList.FaultTime > startTime).all()
    else:
        endTime = datetime.strptime(endTime, "%Y-%m-%d %H:%M:%S")
        result = FaultList.query.filter(FaultList.FaultTime > startTime, FaultList.FaultTime < endTime).all()
    for item in result:
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
    return jsonify(dic)
