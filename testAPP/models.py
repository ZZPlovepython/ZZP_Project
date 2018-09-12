import sys,os
from sqlalchemy import *
from sqlalchemy import create_engine
import sqlalchemy.util as util
import string, sys
from sqlalchemy.databases import mysql
from sqlalchemy import Column, Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


basedir = os.path.abspath(os.path.dirname(__file__))
#engine = create_engine('mysql+pymysql://root:147258@localhost:3306/ceshi?charset=utf8',encoding = "utf-8",echo =True)
engine = create_engine('sqlite:///' + os.path.join(basedir,'data-dev.sqlite'))
Base = declarative_base()
class LogData(Base):
     __tablename__ = 'dataceshi1'

     id = Column(Integer, primary_key=True)
     timestamp = Column(DateTime)
     datatype = Column(Integer)
     datahead = Column(Integer)
     password = Column(Integer)
     datatype = Column(Integer)
     dataheader = Column(Integer)
     AGV_status = Column(Integer)
     cmdstatus = Column(Integer)
     AGVPositation_x = Column(Integer)

Base.metadata.create_all(engine)
