import socket
import os
import time
# 这是爸爸自己写的！ 不是第三方库！
from my_htmlparser import *


'''
# 我把HTML文件写到了一个文本文档里面，用于测试
with open('html.txt', 'r', encoding = 'utf-8') as htmlFile:
    htmlContent = htmlFile.read()
'''
def getHostPath(url):
    # 这一步获取主机和路径
    if url.find("http") >= 0: # 第一种是带http的url, i.e. http://csse.xjtlu.edu.cn
        print(url.split('/', 3))
        host = url.split('/', 3)[2]
        path = url.split('/', 3)[3]
    else: # 第二种是不带的 裸奔的， i.e. csse.xjtlu.edu.cn
        host = url.split('/', 1)[0]
        path = url.split('/', 1)[1]

    # 输入的url可能是不规范的
    if path[-1] != '/':
        path = path + '/'

    return host, path

# 由于每次读取数据都可能超出buffer size, 所以把这块代码封装起来，以便反复利用
def recvData(clientSocket):
    # BufferSize基本上不够一次接受所有数据，所以需要循环来接受完整数据，直到接受的数据为空
    clientSocket.settimeout(1)
    total_data = [] # 存储数据的容器，每次循环就更新一次
    while True:
        try:
            result = clientSocket.recv(4096)
        except:
            break
        '''
        if not result:
            break # 如果result为空 意味着数据接收完了
        '''

        '''
        这里涉及到socket的阻塞问题
        虽然返回了空的数据包，但是socket不知道什么时候结束，他一直会卡在缓冲区，
        一直在等数据
        这导致，老子的socket变成一次性的了
        循环一次后 就用不了了
        '''

        total_data.append(result) # 更新
    result = b''.join(total_data) # 最后将这个list变成str

    return result

# 简化流程
def GET(host, path):
    # HTTP GET请求
    request = "GET /"+ path + " HTTP/1.1\r\nHost: " + host + "\r\nConnection:keep-alive\r\n\r\n"
    request = request.encode()

    return request

def get_html(result):
    head, body = result.split(b'\r\n\r\n', 1) # 将header与body分开 学长是个天才 跟我一样

    return body.decode()

'''
代码逻辑： 
1. 输入url
2. 从url里面得到host和path
3. 根据host和path，获取html界面
4. 根据获取的HTML界面，获取图片源码
5. 根据源码，下载
'''

def downloadImg(url):
    host, path = getHostPath(url)

    # 正常连接过程，HTTP端口为80
    ip_address = socket.gethostbyname(host)
    port = 80
    clientSocket = socket.socket()
    # clientSocket.setblocking(0)
    clientSocket.connect((ip_address, port))

    request = GET(host, path) # 发出的也是二进制数据
    clientSocket.send(request)

    result = recvData(clientSocket) #收到的是二进制数据

    html = get_html(result)

    imgSrc = findSrc('img', html)

    for src in imgSrc:
        print(src)

downloadImg('csse.xjtlu.edu.cn/classes/CSE205')
    # 第一次请求的是HTML文件 所以需要解析，获取图片地址
    #imgSrc = findSrc('img', result.decode())

'''
对于获取的图片地址，应该进行分类处理，
一类是存储在当前目录下的， 另一类是下一层目录下的
'''



# head, body = result.split(b'\r\n\r\n', 1) # 将header与body分开 学长是个天才 跟我一样


'''
file = open('test.jpg', 'wb')
file.write(body)
file.close()

print("Done! ")
# print(findSrc('img', result))
'''

'''

while True:
    # 接下来的和UDP基本一样了
    print("Connect succeed!")

    clientSocket.sendall(httpCom.encode())

    print(clientSocket.recv(1024).decode())
    


clientSocket.close()
print('Connection closed')
'''