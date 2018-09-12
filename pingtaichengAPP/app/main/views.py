#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from flask import render_template, session, redirect, url_for, flash, abort, request, jsonify
from . import main
from .. import db
from ..models import SetPoint, NewData, FaultList, aftercheck_list, Diagnosis


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


@main.route('/', methods=['POST', 'GET'])
def index():
    result = SetPoint.query.order_by(SetPoint.Timestamp.desc()).first()
    if not(result):
        flash('请先进行参数设定')
    return render_template('RunningUI.html')


@main.route('/data', methods=['POST', 'GET'])
def data():
    dic = {}
    sencer = ['Tag1', 'Tag2', 'Tag3', 'Tag4']
    resultNow = NewData.query.order_by(NewData.Timestamp.desc()).first()
    resultFault = Diagnosis.query.order_by(Diagnosis.Timestamp.desc()).first()
    fault_num = aftercheck_list.query.filter_by(state_fault=1).count()
    alarm_num = aftercheck_list.query.filter_by(state_prealarm=1).count()
    normal_num = aftercheck_list.query.filter_by(state_normal=1).count()
    all_num = aftercheck_list.query.count()
    resultstate = aftercheck_list.query.order_by(aftercheck_list.Timestamp.desc()).first()
    dic['weight'] = getattr(resultNow, 'Weight')
    dic['run_time'] = time_transform(all_num)
    dic['fault_time'] = time_transform(fault_num)
    dic['alarm_time'] = time_transform(alarm_num)
    dic['normal_time'] = time_transform(normal_num)
    dic['timestr'] = resultFault.Timestamp.strftime('%Y-%m-%d %H:%M:%S')
    dic['falutmsg'] = ''
    if resultstate.state_fault:
        dic['state'] = 'fault'
    elif resultstate.state_prealarm:
        dic['state'] = 'alarm'
    elif resultstate.state_normal:
        dic['state'] = 'normal'
    for item in sencer:
        dic[item] = getattr(resultNow, 'Weight' + item)
        if getattr(resultFault, item + 'Loss'):
            dic['falutmsg'] += 'Weight' + item + '信号丢失故障<br/>'
            dic[item + 'Loss'] = 1
        if getattr(resultFault, item + 'Forced'):
            dic['falutmsg'] += 'Weight' + item + '瞬时受力报警<br/>'
            dic[item + 'Forced'] = 1
        if getattr(resultFault, item + 'Partial'):
            dic['falutmsg'] += 'Weight' + item + '偏载报警<br/>'
            dic[item + 'Partial'] = 1
        if getattr(resultFault, item + 'Over') == 3:
            dic['falutmsg'] += 'Weight' + item + '瞬时过流故障<br/>'
            dic[item + 'tempOver'] = 1
        elif getattr(resultFault, item + 'Over') == 4:
            dic['falutmsg'] += 'Weight' + item + '超出量程故障<br/>'
            dic[item + 'Over'] = 1
    return jsonify(dic)
