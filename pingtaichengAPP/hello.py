#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column
from sqlalchemy.types import CHAR, Integer, String
from sqlalchemy.ext.declarative import declarative_base

DB_CONNECT_STRING = 'mysql+pymysql://root:147258@localhost/ceshi'
engine = create_engine(DB_CONNECT_STRING, echo=True)
DB_Session = sessionmaker(bind=engine)
session = DB_Session()

#session.execute('create database abc')
print (session.execute('select name from users').fetchall())
#BaseModel = declarative_base()

'''def init_db():
    BaseModel.metadata.create_all(engine)

def drop_db():
    BaseModel.metadata.drop_all(engine)


class User(BaseModel):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(CHAR(30)) # or Column(String(30))

init_db()'''