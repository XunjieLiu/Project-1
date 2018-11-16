import socket
import os
import time
import threading
# 这是爸爸自己写的！ 不是第三方库！
from my_htmlparser import *

depth = 1
oldPages = []

'''
# 我把HTML文件写到了一个文本文档里面，用于测试
with open('html.txt', 'r', encoding = 'utf-8') as htmlFile:
    htmlContent = htmlFile.read()
'''
def getHostPath(url):
    # 这一步获取主机和路径
    if url.find("http") >= 0: # 第一种是带http的url, i.e. http://csse.xjtlu.edu.cn
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

def saveImg(url, clientSocket, html):
    host, path = getHostPath(url)
    imgSrc = findSrc('img', html)

    print("Src found")

    rootPath = os.getcwd()
    currentPath = os.getcwd()

    for src in imgSrc:
        imgPath = path + src
        
        request = GET(host, imgPath)
        clientSocket.send(request)
        print("Start requesting for image data")
        result = recvData(clientSocket)
        print("Image data recieved")
        head, body = result.split(b'\r\n\r\n', 1) # 将header与body分开 学长是个天才 跟我一样

        folders = [] # 存储文件夹的名字，顺序就是深度，最后一个是文件名
        imgPath = url + src # 处理绝对路径与相对路径

        # 将imgPath解析，提取文件名
        for i in imgPath.split('/'):
            if i != '' and i != 'http:':
                folders.append(i)
        # folders = ['csse.xjtlu.edu.cn', 'classes', 'CSE205', 'testImages', 'upside-down-cat-thumbnail.jpg'] 
        # 文件名
        name = imgPath.split('/')[-1]

        for folder in folders:
            if folder == name:
                break 

            if os.path.exists(folder): # 文件夹可能已经存在了
                print('File exists')
            else:
                os.mkdir(folder) # 不存在的话 新建一个

            # 然后跳到下一层文件夹里面
            currentPath = currentPath + '\\' + folder
            os.chdir(currentPath) # Jump！

        # 观众朋友们大家好 现在我们来到了最底层文件夹，你们可以放下手里的图片了
        # 如果有重名的图片 请把名字改到不重名为止
        while(os.path.isfile(name)):
            name = 'copy_' + name

        # 一通操作 文件写好了
        file = open(name, 'wb')
        file.write(body)
        file.close()
        os.chdir(rootPath) # 回到根目录 我们准备开始下一次旅行
        currentPath = rootPath # 请大家更新一下手中的地图 别走岔了

def downloadImg(url):
    host, path = getHostPath(url)

    # 正常连接过程，HTTP端口为80
    ip_address = socket.gethostbyname(host)
    port = 80
    clientSocket = socket.socket()
    # clientSocket.setblocking(0)
    clientSocket.connect((ip_address, port))

    print('Connection succeed')

    request = GET(host, path) # 发出的也是二进制数据
    clientSocket.send(request)

    print("Start recieve html data")

    result = recvData(clientSocket) # 收到的是二进制数据

    print('Data recieved')

    html = get_html(result)

    saveImg(url, clientSocket, html)

# downloadImg('http://www.xjtlu.edu.cn/en/departments/academic-departments/computer-science-and-software-engineering/')
downloadImg('http://csse.xjtlu.edu.cn/classes/CSE205')

