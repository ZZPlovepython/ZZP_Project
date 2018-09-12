#!/user/bin/env python3
# -*- coding:utf-8 -*-
from sqlalchemy import *
from sqlalchemy import create_engine
import sqlalchemy.util as util
import string, sys
from sqlalchemy.databases import mysql
from sqlalchemy import Column, Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


'''mysql_engine = create_engine('mysql://root:147258@localhost:3306/ceshi?charset=utf8',\
	encoding = "utf-8",echo =True)   
#mysql_engine.connect()    
metadata = MetaData()


#创建users表
users_table = Table('users', metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String(20), nullable = False),
    Column('fullname', String(20), nullable = False),
    Column('password', String(20), nullable = False),
    mysql_engine='InnoDB'
)


#mysql_engine='InnoDB' 或者 mysql_engine='MyISAM' 表类型
metadata.create_all(mysql_engine)#方法1'''
engine = create_engine('mysql+pymysql://root:147258@localhost:3306/ceshi?charset=utf8',encoding = "utf-8",echo =True)
Base = declarative_base()
class User(Base):
     __tablename__ = 'users'

     id = Column(Integer, primary_key=True)
     name = Column(String(20))
     fullname = Column(String(40))
     password = Column(String(12))

Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()
session.add_all([User(name='wendy', fullname='Wendy Williams', password='foobar'),\
                 User(name='mary', fullname='Mary Contrary', password='xxg527'),\
                 User(name='lisa', fullname='lisa Contrary', password='ls123'),\
                 User(name='cred', fullname='cred Flinstone', password='bla123'),\
                 User(name='fred', fullname='Fred Flinstone', password='blah')])
# 提交即保存到数据库:
session.commit()
# 关闭session:b
