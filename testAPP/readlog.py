#!/usr/bin/env python3
from math import exp,log,sqrt
from numpy import *
import re,os
import time
from datetime import date,time,datetime
from operator import itemgetter
import sys
from sqlalchemy import *
from sqlalchemy import create_engine
import sqlalchemy.util as util
import string, sys
from sqlalchemy.databases import mysql
from sqlalchemy import Column, Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

year = []
month = []
day = []
hour = []
minute = []
second = []
minsecond = []
current_time = []
datatype = []
dataheader =[]
AGV_status = []
cmdstatus =[]
AGVPositation_x = []
status_cmd = []
frametype = []
status_ls = []
status_gyrozero = []
status_bucket = []
status_barcode = []
status_motorenable = []



basedir = os.path.abspath(os.path.dirname(__file__))
#engine = create_engine('mysql+pymysql://root:147258@localhost:3306/ceshi?charset=utf8',encoding = "utf-8",echo =True)
Base = declarative_base()
engine = create_engine('sqlite:///' + os.path.join(basedir,'data-dev.sqlite'))

class LogData(Base):
     __tablename__ = 'NormalFrameList'

     id = Column(Integer, primary_key=True)
     timestamp = Column(DateTime)
     datatype = Column(Integer)
     dataheader = Column(Integer)
     AGV_status = Column(Integer)
     cmdstatus = Column(Integer)
     AGVPositation_x = Column(Integer)
     status_cmd = Column(Integer)
     frametype = Column(Integer)
     status_ls = Column(Integer)
     status_gyrozero = Column(Integer)
     status_bucket = Column(Integer)
     status_barcode = Column(Integer)
     status_motorenable = Column(Integer)

Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)
session = DBSession()


#file_reader = open('D:/anzhuangbao/work/20180502000000.txt','r')
file_object = open('D:/work files/93/20180502000000', 'rb')
try:
	while True:
		buff = file_object.read()
		if not buff:
			break
		fsize = len(buff)
		itemnum = int(fsize/58)
		for i in range(1000):
			year1 = buff[0+i*58]
			year2 = buff[1+i*58]
			year.append(16**2*year1+year2)
			month.append(buff[2+i*58])
			day.append(buff[3+i*58])
			hour.append(buff[4+i*58])
			minute.append(buff[5+i*58])
			second.append(buff[6+i*58])
			minsecond.append(16**2*buff[7+i*58]+buff[8+i*58])
			datatype.append(buff[9+i*58])#数据类型
			dataheader.append(buff[10+i*58])#数据帧头
			AGV_status.append(buff[11+i*58])#车辆状态
			cmdstatus.append(buff[12+i*58])#命令状态
			frametype.append(int(uint8(cmdstatus[i]<<3)>>7))#数据帧类型：1-特殊帧，0-正常帧
			status_cmd.append(int(uint8(AGV_status[i]<<6)>>6))#指令执行状态：0-命令执行完成，1-命令执行中，2-接受到错误指令，3-指令因错误终止
			status_ls.append(int(uint8(AGV_status[i]<<5)>>7))#顶升限位确认状态：1-已确认，0-未确认
			status_gyrozero.append(int(uint8(AGV_status[i]<<4)>>7))#GYO零偏纠正状态：1-完成，0-未完成
			status_bucket.append(int(uint8(AGV_status[i]<<2)>>6))#带载状态：0-没带货架；1-带货架；2-不确定
			status_barcode.append(int(uint8(AGV_status[i]<<1)>>7))#地面标码读取状态：1-已读到，0-没读到
			status_motorenable.append(int(uint8(AGV_status[i]>>7)))#电机使能状态：1-使能，0-禁止
			AGVPositation_x.append(buff[13+i*58]*16**6+buff[14+i*58]*16**4+buff[15+i*58]*16**2+buff[16+i*58])
			s = str(year[i]) + "-" + str(month[i])+"-"+str(day[i])+" "+str(hour[i])+":"+str(minute[i])+":"+\
				str(second[i])+":"+str(minsecond[i])
			current_time = datetime.strptime(s,'%Y-%m-%d %H:%M:%S:%f')
			print (datetime.strptime(s,'%Y-%m-%d %H:%M:%S:%f'),cmdstatus[i],status_cmd[i],frametype[i],AGVPositation_x[i])
			p = LogData(timestamp=current_time,datatype=datatype[i],dataheader=dataheader[i],AGV_status=AGV_status[i],\
				cmdstatus=cmdstatus[i],AGVPositation_x=AGVPositation_x[i],frametype=frametype[i],status_cmd=status_cmd[i],\
				status_ls=status_ls[i],status_gyrozero=status_gyrozero[i],status_bucket=status_bucket[i],status_barcode=status_barcode[i],\
				status_motorenable=status_motorenable[i])
			session.add(p)
			session.commit()
			print (type(status_cmd[i]),type(cmdstatus[i]))
		#current_time1 = datetime.strptime(s, '%Y/%m-%d') 
finally:
    file_object.close()
session.commit()
print (current_time)


poltdata = []
polttime = []
begin = "2018"+"-"+"05"+"-"+"02"+" "+"00"+":"+"00"+":"+"01"+":"+"450"
begin_time = datetime.strptime(begin,'%Y-%m-%d %H:%M:%S:%f')
data = session.query(LogData)
for item in data:
	if item.timestamp<begin_time:
		polttime.append(item.timestamp)
		poltdata.append(item.cmdstatus)
	else:
		break
print (polttime,poltdata)