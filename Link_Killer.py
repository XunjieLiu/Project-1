from Image_Killer import *
import socket
from my_htmlparser import *

# absolute_path = [] # 存储着所有已被访问的链接
root = 'http://csse.xjtlu.edu.cn/classes/CSE205/'
url1 = 'http://csse.xjtlu.edu.cn/classes/CSE205/sub1/'
url2 = 'http://csse.xjtlu.edu.cn/classes/CSE205/sub1/subsub1'
url3 = 'http://csse.xjtlu.edu.cn/classes/CSE205/sub1/subsub1.2'
url4 = 'http://csse.xjtlu.edu.cn/classes/CSE205/sub4/'

'''
list = []
list.append(root)
list.append(url1)
list.append(url2)
list.append(url3)
list.append(url4)
'''

'''
第一步 ： get_html()
第二步 ： get_links()
第三步： 存进去

重复以上步骤 直到深度为5的所有不重复链接都找到为止
'''


'''
会有：sub/subsub1这种链接，也会有/classes/CSE205/sub这种
'''
def test(url):
    clientSocket = get_socket(url)

    if clientSocket == 0:
        return False

    host, path = get_host_path(url)
    if path[-1] == '/':
        path = path[:-1]
    request = GET(host, path)
    clientSocket.send(request)
    result = clientSocket.recv(4096)
    head, body = result.split(b'\r\n\r\n', 1)

    if head.decode().split('\r\n', 1)[0].find('200') >= 0:
        return True
    else:
        print(head.decode().split('\r\n', 1)[0])
        return False
        

def get_links(html, url, absolute_path):
    relative_path = findAll('a', html)
    host, path = get_host_path(root)
    # 如果relative_path 里面含有/classes/CSE205,说明这个链接需要和host相连

    if len(relative_path) == 0:
        print("Not link here")
        return

    if url[-1] != '/':
        url = url + '/'

    for link_path in relative_path:
        if link_path.find(path) >= 0:
            # print(link_path)
            # link_path = link_path.split(path)[1]
            temp = 'http://' + host + '/' + link_path
        else:
            temp = url + link_path

        if temp in absolute_path:
            print("Exists!")
        else:
            if test(temp):
                absolute_path.append(temp)

def link_killer(root, depth):
    absolute_path = [] # 存储着所有已被访问的链接
    root_html = get_html(root)
    get_links(root_html, root, absolute_path)

    temp_list = []

    if depth < 1:
        return

    for i in range(depth):
        for path in absolute_path:
            if path in temp_list:
                continue
            else:
                temp_list.append(path)

        for temp in temp_list:
            html = get_html(temp)
            get_links(html, root, absolute_path)

    return absolute_path

# absolute_path = link_killer(root, 3)
'''
tempList = []

for i in absolute_path:
    if i in tempList:
        continue
    else:
        tempList.append(i)

for i in tempList:
    html = get_html(i)
    get_links(html, root)

for i in absolute_path:
    if i in tempList:
        continue
    else:
        tempList.append(i)

for i in tempList:
    html = get_html(i)
    get_links(html, root)
'''
'''
killer1 = Image_Killer(root)
killer1.run()

killer2 = Image_Killer(url1)
killer2.run()
'''

if __name__ == '__main__': 
    killer = Image_Killer(url2, root)
    killer.run()


        