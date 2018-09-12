#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_sqlalchemy import flask_sqlalchemy
import pymysql

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI '] = 'mysql+pymysql://root:147258@localhost/ceshi1'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLALchemy(app)

class SetPoint(db.Model):
    __tablename__ = 'setpoint'
    ID = db.Column(db.Integer, primary_key=True)
    SencerNum = db.Column(db.Integer)S
    SencerName = db.Column(db.String(125))