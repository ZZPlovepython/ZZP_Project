#!/usr/bin/env python
# -*- coding: utf-8 -*-
from . import db
import datetime
# import itertools
# import random


class SetPoint(db.Model):
    __tablename__ = 'setpoint'
    ID = db.Column(db.Integer, primary_key=True)
    SencerNum = db.Column(db.Integer)
    SencerName = db.Column(db.String(125))
    EqpNum = db.Column(db.String(125))
    Timestamp = db.Column(db.DateTime, default=datetime.datetime.now, index=True)
    NoLoad_set = db.Column(db.String(100))
    EmptyLoad_set = db.Column(db.String(100))
    Temp = db.Column(db.Float)
    Wet = db.Column(db.Float)
    ExcV = db.Column(db.Float)
    Sensitivity = db.Column(db.Float)
    Resistance = db.Column(db.Integer)
    Supplier = db.Column(db.String(100))


class NewData(db.Model):
    __tablename__ = 'newdata'
    ID = db.Column(db.Integer, primary_key=True)
    Timestamp = db.Column(db.DateTime, default=datetime.datetime.now, index=True)
    WeightTag1 = db.Column(db.Float)
    WeightTag2 = db.Column(db.Float)
    WeightTag3 = db.Column(db.Float)
    WeightTag4 = db.Column(db.Float)
    Weight = db.Column(db.Float)


class Diagnosis(db.Model):
    __tablename__ = 'diagnosis'
    ID = db.Column(db.Integer, primary_key=True)
    Timestamp = db.Column(db.DateTime, default=datetime.datetime.now, index=True)
    Tag1Loss = db.Column(db.Integer, default=0)
    Tag2Loss = db.Column(db.Integer, default=0)
    Tag3Loss = db.Column(db.Integer, default=0)
    Tag4Loss = db.Column(db.Integer, default=0)
    Tag1Over = db.Column(db.Integer, default=0)
    Tag2Over = db.Column(db.Integer, default=0)
    Tag3Over = db.Column(db.Integer, default=0)
    Tag4Over = db.Column(db.Integer, default=0)
    Tag1Forced = db.Column(db.Integer, default=0)
    Tag2Forced = db.Column(db.Integer, default=0)
    Tag3Forced = db.Column(db.Integer, default=0)
    Tag4Forced = db.Column(db.Integer, default=0)
    Tag1Partial = db.Column(db.Integer, default=0)
    Tag2Partial = db.Column(db.Integer, default=0)
    Tag3Partial = db.Column(db.Integer, default=0)
    Tag4Partial = db.Column(db.Integer, default=0)
    ScaleState = db.Column(db.Integer, default=0)


class FaultList(db.Model):
    __tablename__ = 'faultlist'
    ID = db.Column(db.Integer, primary_key=True)
    FaultTime = db.Column(db.DateTime, default=datetime.datetime.now, index=True)
    RecoverTime = db.Column(db.DateTime)
    PeriodSecond = db.Column(db.Integer)
    FaultSencer = db.Column(db.String(20), index=True)
    FaultCode = db.Column(db.Integer, index=True)
    FaultState = db.Column(db.Boolean)


class aftercheck_list(db.Model):
    __tablename__ = 'checkedlist'
    ID = db.Column(db.Integer, primary_key=True)
    Timestamp = db.Column(db.DateTime, default=datetime.datetime.now, index=True)
    state_fault = db.Column(db.Boolean, default=0)
    state_normal = db.Column(db.Boolean, default=0)
    state_prealarm = db.Column(db.Boolean, default=0)


class OperationRecord(db.Model):
    __tablename__ = 'operationrecord'
    ID = db.Column(db.Integer, primary_key=True)
    Timestamp = db.Column(db.DateTime, default=datetime.datetime.now, index=True)
    record = db.Column(db.String(250))
    standard = db.Column(db.Float)
    zeropoint = db.Column(db.Float)
