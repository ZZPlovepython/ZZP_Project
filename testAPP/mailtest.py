#!/usr/bin/python
# coding=utf-8
import smtplib
from email.mime.text import MIMEText
from email.header import Header

subject = '不放假通知'
msg = MIMEText('hello, send by Python...', 'plain', 'utf-8')
msg['Subject'] = Header(subject, 'utf-8')  
msg['From'] = 'zzp<zzp20180407@163.com>'    
msg['To'] = "1162645284@qq.com"

# 输入Email地址和口令:
from_addr = "zzp20180407@163.com"
password = "zzpskq520"
# 输入SMTP服务器地址:
smtp_server = "smtp.163.com"
# 输入收件人地址:
to_addr = "1162645284@qq.com"

server = smtplib.SMTP(smtp_server, 25) # SMTP协议默认端口是25
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()