import socket
import re

host = "csse.xjtlu.edu.cn"
ipaddress=socket.gethostbyname("csse.xjtlu.edu.cn")
port = 80
clientSocket = socket.socket()
clientSocket.connect((ipaddress,port))
request = 'GET /classes/CSE205/ HTTP/1.1\r\nHost: csse.xjtlu.edu.cn\r\n\r\n'
clientSocket.send(request.encode())

result = clientSocket.recv(8192).decode()

'''
totoal_data = [] 
while True:
    result = clientSocket.recv(4096)
    if not result:
        break 

    totoal_data.append(result) 
result = b''.join(totoal_data) 
'''

print(result)
