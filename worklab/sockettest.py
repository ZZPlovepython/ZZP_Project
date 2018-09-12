'''import socket
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('http://30.113.149.133',7171))'''
'''import websocket
ws = websocket.WebSocket()
ws.connect("ws://30.113.149.133:7171",http_proxy_host="http://30.113.149.133", http_proxy_port=7171)'''
from websocket import create_connection
ws = create_connection("ws://30.113.149.133:7171",http_proxy_host="http://30.113.149.133", http_proxy_port=7171)

data = '''GET http://30.113.149.133
Host: http://30.113.149.133
Connection: keep-alive
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36
Accept-Language: zh-CN,zh;q=0.8
'''

s.send(data.encode())
buf=s.recv(16)
while len(buf):
    buf = s.recv(16)
print (buf)