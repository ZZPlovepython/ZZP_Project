#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
from socket import *
import re
from datetime import datetime
HOST = ''
PORT = 2000  # 设置侦听端口
BUFSIZ = 2048
ADDR = (HOST, PORT)
sock = socket(AF_INET, SOCK_STREAM)

sock.bind(ADDR)

sock.listen(5)
STOP_CHAT = False
while not STOP_CHAT:
    print('wait and binding:%d' % (PORT))
    tcpClientSock, addr = sock.accept()
    # tcpClientSock.settimeout(0.0)
    print('accepted, client address is：', addr)
    while True:
        data_str = tcpClientSock.recv(BUFSIZ)
        # listdata = data_str.split(',')[:3]
        listdata = re.findall(r"\d+\.?\d*", data_str)
        listread = [float(x) / 100 for x in listdata]
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print listread
