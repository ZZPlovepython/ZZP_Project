#!/usr/bin/python  
#coding=utf-8  
  
  
import socket  
#import fcntl  
import struct  

'''def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])
  
  
if __name__ == '__main__':
	print (get_ip_address('lo')) #环回地址 
	print (get_ip_address('eth0')) #主机ip地址'''
import socket

'''hostname = socket.gethostname()

IPinfo = socket.gethostbyname_ex(hostname)

LocalIP = IPinfo[2][0]  # [2][0] 2保持不变，如果删除[0]会输出本机所有网卡获取的IP地址，[0]为0时获取的是本地连接的IP地址，有待测试。

print (LocalIP)'''
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 80))
ip = s.getsockname()[0]
print (type(ip))
