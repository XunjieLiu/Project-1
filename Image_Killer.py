import socket
import os
import time
import threading
import re

url = 'http://csse.xjtlu.edu.cn/classes/CSE205'
url2 = 'http://csse.xjtlu.edu.cn/classes/CSE205/sub1/'

# This method will return all complete segments with corresponding tag
# Like findAll(img, html) ----> <img src = "blablabla" />
def findAll(tag, htmlText):
    if tag == 'img':
        pattern = r'(src.?=.?".+?[\.jpg|\.jpeg|\.png|\.gif|\.webp]")'
    elif tag == 'a':
        pattern = r'<a.*(href.?=.?".*").*>.*</a>'
    else:
        return []

    result = re.findall(pattern, htmlText)

    
    if len(result) != 0:
        for i in range(len(result)):
            temp = result[i].split('"')[1]
            result[i] = temp

            if result[i][0] == '/':
                result[i] = result[i][1:]

        '''
        返回的src可能是这样的：/en/assets/image-cache/templates/xjtlu/img/hero-image-default-1.9cdb9aa2.jpg
        也可能是这样的：testImages/upside-down-cat-thumbnail.jpg
        我们只接受第二种，所以需要对第一种进行操作
        '''
        return result
    else:
        return []

'''
def get_html(url) 建立连接，返回HTML文件
def get_img_src(html, url) 解析HTML，返回img的路径，与url一结合，就是绝对路径
def download_img(imgSrc) 根据图片的绝对路径，下载图片
'''
# 简化流程
def GET(host, path):
    # HTTP GET请求
    request = "GET /"+ path + " HTTP/1.1\r\nHost: " + host + "\r\nConnection:keep-alive\r\n\r\n"
    request = request.encode()
    print(request)

    return request # 返回的也是二进制数据

# 由于每次读取数据都可能超出buffer size, 所以把这块代码封装起来，以便反复利用
def recvData(clientSocket):
    # BufferSize基本上不够一次接受所有数据，所以需要循环来接受完整数据，直到接受的数据为空
    clientSocket.settimeout(0.5)
    total_data = [] # 存储数据的容器，每次循环就更新一次

    try:
        # 如果是完全不符合HTTP协议的请求，recv毛都收不到
        result = clientSocket.recv(4096)
        head, body = result.split(b'\r\n\r\n', 1) # 将header与body分开 学长是个天才 跟我一样
    except:
        print("Exception! ")
        return []

    print(head.decode().split('\r\n', 1)[0])

    if head.decode().split('\r\n', 1)[0].find('200') >= 0:
        total_data.append(result)
    else:
        print('Nothing')
        return []

    print("HTTP OK")
    while True:
        try:
            result = clientSocket.recv(4096)
            if not result:
                break # 如果result为空 意味着数据接收完了
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

def get_host_path(url):
    if len(url.split('/')) == 1:
        host = url
        path = '/'

        return host, path
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

    return host, path # ('csse.xjtlu.edu.cn', 'classes/CSE205/') 结尾一定会有'/'

def get_socket(url):
    try:
        host, path = get_host_path(url) # 解析url 得到'csse.xjtlu.edu.cn', 'classes/CSE205/'

        # 正常连接过程，HTTP端口为80
        ip_address = socket.gethostbyname(host)
        port = 80
        clientSocket = socket.socket()
        # clientSocket.setblocking(0)
        clientSocket.connect((ip_address, port))

        return clientSocket
    except:
        return 0

def get_html(url):
    host, path = get_host_path(url) # 解析url 得到'csse.xjtlu.edu.cn', 'classes/CSE205/'
    if get_socket(url) == 0:
        print("Invalid url!")
    else:
        clientSocket = get_socket(url)
        print('Connection succeed')

    request = GET(host, path) # 发出的也是二进制数据
    print(request)
    clientSocket.send(request)

    print("Start recieve html data")
    result = recvData(clientSocket) # 收到的是二进制数据
    clientSocket.close()
    print('Data recieved')

    try:     
        head, html = result.split(b'\r\n\r\n', 1) # 将header与body分开 学长是个天才 跟我一样
    except:
        print(url)
        print("This url maybe invalid")
        return

    # 可能返回的html界面是404， 所以需要分析一下HTTP回复报文
    if head.decode().split('\r\n', 1)[0].find('200') >= 0:
        # saveImg(url, clientSocket, html.decode())
        return html.decode()
    else:
        print(head.decode().split('\r\n', 1)[0])

def get_img_src(url, html):
    try:
        host, path = get_host_path(url)
        relativePath = findAll('img', html)

        rootPath = []

        for src in relativePath:
            root = url + '/' + src
            print(root)
            rootPath.append(root)

        return rootPath
    except:
        print("Cannot get img src")

def get_img(url, rootPath):
    try:
        clientSocket = get_socket(url)

        for src in rootPath:
            host, path = get_host_path(src)

            '''
            如果是图片文件，GET请求里面路径后面不可以带／
            '''

            if path[-1] == '/':
                path = path[:-1]
            print(path)
            request = GET(host, path)
            clientSocket.send(request)
            print("Start requesting for image data")
            result = recvData(clientSocket)

            if len(result) < 1:
                continue # 图片内容可能啥都没有

            print("Image data recieved")
            head, body = result.split(b'\r\n\r\n', 1) # 获取图片二进制数据
            name = src.split('/')[-1]

            save_img(src, body, url)
    except Exception as e:
        print("Exception in get_img method")
        print(e)

def save_img(src, data, url):
    rootPath = os.getcwd()
    currentPath = os.getcwd()
    folders = [] # 存储文件夹的名字，顺序就是深度，最后一个是文件名
    # 将imgPath解析，提取文件名
    for i in url.split('/'):
        if i != '' and i != 'http:':
            folders.append(i)
    # folders = ['csse.xjtlu.edu.cn', 'classes', 'CSE205', 'testImages', 'upside-down-cat-thumbnail.jpg'] 
    # 文件名
    name = src.split('/')[-1]

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
    file.write(data)
    file.close()
    os.chdir(rootPath) # 回到根目录 我们准备开始下一次旅行
    currentPath = rootPath # 请大家更新一下手中的地图 别走岔了

class Image_Killer(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url
        self.depth = depth

    def run(self):
        html = get_html(self.url)
        rootSrc = get_img_src(self.url, html)
        get_img(self.url, rootSrc)


# Killer = Image_Killer(url)
# Killer.run()

'''
我可以先把所有的sub都爬下来呀 然后挨个下载不就可以了
'''


