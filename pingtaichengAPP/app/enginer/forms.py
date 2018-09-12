#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextField, SelectField, TextAreaField
from wtforms.validators import Required, Length, Email, Regexp, ValidationError


class SetForm(Form):
    Num = StringField('传感器数量：', validators=[Required()], render_kw={"placeholder": ""})
    Name = StringField('传感器位号：', validators=[Required()], render_kw={"placeholder": "不同位号间，以逗号分隔"})
    noLoad = StringField('传感器无负载读数：', validators=[Required()], render_kw={"placeholder": "数值间，以逗号分隔"})
    emptyLoad = StringField('传感器空载读数：', validators=[Required()], render_kw={"placeholder": "数值间，以逗号分隔"})    
    ExcV = StringField('激励电压(mV)：', validators=[Required()], render_kw={"placeholder": ""})
    Sensitivity = StringField('传感器灵敏度(mV)：', validators=[Required()], render_kw={"placeholder": ""})
    Resistance = StringField('传感器阻抗(Ω)：', validators=[Required()], render_kw={"placeholder": ""})
    Temp = StringField('记录时环境温度(℃)：', validators=[Required()], render_kw={"placeholder": ""})
    Wet = StringField('记录时环境湿度(%)：', validators=[Required()], render_kw={"placeholder": ""})
    # submit = SubmitField('提交信息')

    def __init__(self, *args, **kwargs):
        super(SetForm, self).__init__(*args, **kwargs)


class InfoForm(Form):
    eqpName = StringField('设备号：', validators=[Required()], render_kw={"placeholder": ""})
    productInfo = StringField('制造商信息：', validators=[Required()], render_kw={"placeholder": ""})


class OperationForm(Form):
    date = StringField('操作时间：', validators=[Required()], render_kw={"placeholder": "year-month-day hour:month"})
    operate = TextAreaField('操作记录：', validators=[Required()], render_kw={"placeholder": "请填写操作记录"})
    standard = StringField('操作时标定值：', validators=[Required()], render_kw={"placeholder": ""})
    zero = StringField('操作时零点值：', validators=[Required()], render_kw={"placeholder": ""})
    submit = SubmitField('提交信息')


class HistoryForm(Form):
    startdate = StringField('起始时间：', validators=[Required()], render_kw={"placeholder": "year-month-day hour:month"})
    enddate = StringField('结束时间：', validators=[Required()], render_kw={"placeholder": "year-month-day hour:month"})
    submit = SubmitField('查询')
