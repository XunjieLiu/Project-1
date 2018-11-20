import gzip, socket, re, os, threading, ssl, zlib


def get_html(domain: str):
    print(">>> Getting HTML files... from {}".format(domain))
    host, port, path = get_host_port_path(domain)
    body = get_http_body(host, port, path)
    try:
        temp = gzip.decompress(body)
        body = temp
        print('OK')
    except Exception as en:
        print(domain)
        print('Warning get_html: ' + str(en))
    return body.decode()


def get_http_body(host, port, path):
    try:
        ip = socket.gethostbyname(host)
        if port == 0:
            raise Exception("Error: Domain is not acceptable! (only http/https)")
        if port == 80:
            se = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            se.connect((ip, port))
        else:
            se = ssl.wrap_socket(socket.socket())
            se.connect((ip, port))

        se.settimeout(20)
        se.send(b"GET " + path.encode() + b" HTTP/1.1\r\n")
        se.send(b"Host: " + host.encode() + b"\r\n")
        se.send(b'Connection:keep-alive\r\n')
        se.send(b"Cache-Control:max-age=0\r\n")
        se.send(b"Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n")
        se.send(b"Upgrade-Insecure-Requests:1\r\n")
        se.send(
            b"User-Agent:Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36\r\n")
        se.send(b"Accept-Encoding:gzip,deflate,sdch\r\n")
        se.send(b"Accept-Language:zh-CN,zh;q=0.8\r\n")
        se.send(b"\r\n")
        # se.send(b"GET http://www.baidu.com HTTP/1.1\r\n")
        buffer = []
        while True:
            d = se.recv(1024)
            if d:
                buffer.append(d)
            else:
                break
        data = b''.join(buffer)
        se.close()
        head, body = data.split(b'\r\n\r\n', 1)
        return body
    except Exception as e:
        print(e)
        return 'Error Http'


def get_host_port_path(domain: str):
    lash_list = domain.split('/')
    # print(lash_list)
    main_domain = lash_list[2]
    path = ""
    for i in range(3, len(lash_list)):
        path += '/' + lash_list[i]
    if domain[:6] == 'http:/':
        port = 80
    elif domain[:6] == 'https:':
        port = 443
    else:
        # raise Exception('not correct domain!')
        port = 0
        pass
    return main_domain, port, path


def get_imgs_list(html):
    # patten = r'<img.*(src.?=.?".*").*\n*>'
    patten = r'(src.?=.?".+?[\.jpg|\.jpeg|\.png|\.gif|\.webp]")'
    ls = re.findall(patten, html)
    paths = []
    for i in ls:
        t = i.split('"')[1]
        paths.append(t)
    return paths


def get_href_list(html):
    patten = r'<a.*(href.?=.?".*").*>.*</a>'
    ls = re.findall(patten, html)
    hrefs = []
    for i in ls:
        t = i.split('"')[1]
        hrefs.append(t)
    return hrefs


class Creeper(threading.Thread):
    def __init__(self, domain, layer=5):
        threading.Thread.__init__(self)
        self.layer = layer
        self.host, self.port, self.path = get_host_port_path(domain)
        self.absoluteRoot = domain
        creeped_pages.append(domain)

        if self.create_dir():
            self.parent_html = get_html(domain)
            self.downloaded_images = []

    def create_dir(self):
        self.current_dir = self.host + '/'.join(self.path.split('/')[:-1]) + '/'
        if os.path.exists(self.current_dir):
            return True
        else:
            try:
                os.makedirs(self.current_dir)
                return True
            except Exception as e:
                return False

    def get_absolute_dirct(self, href_list: list):
        ret_list = []
        for i in range(len(href_list)):
            item = href_list[i]
            if item[:2] == '//':
                absoluteRoot = 'http:' + item
            elif item[:4] == 'http':
                absoluteRoot = item
            elif item[:5] == 'https':
                absoluteRoot = item
            elif item[:1] == '/':
                if self.port == 80:
                    absoluteRoot = 'http://' + self.host + item
                elif self.port == 433:
                    absoluteRoot = 'https://' + self.host + item
            else:
                if self.port == 80:
                    absoluteRoot = 'http://' + self.host + self.path + item
                elif self.port == 443:
                    absoluteRoot = 'https://' + self.host + self.path + item
            if not absoluteRoot[-1] == '/':
                absoluteRoot = absoluteRoot + '/'
            ret_list.append(absoluteRoot)
        return ret_list

    def download_image(self, file_domain):
        host, port, file_path = get_host_port_path(file_domain)
        body = get_http_body(host, port, file_path)
        file_name = self.current_dir + file_domain.split('/')[-1]

        try:
            if os.path.isfile(file_name):
                print('At >>> ' + self.current_dir)
                return True
            else:
                file = open(file_name, 'wb')
                file.write(body)
                file.close()
                print('At >>> ' + self.current_dir)
                return True
        except Exception as e:
            print("Error download_image: " + str(e))
            return False

    def getImageAbsList(self):
        raw_dict_list = get_imgs_list(self.parent_html)
        return self.get_absolute_dirct(raw_dict_list)

    def getSrcList(self):
        raw_dict_list = get_href_list(self.parent_html)
        absolute_dict_list = self.get_absolute_dirct(raw_dict_list)
        ans_dict_list = []
        for i in absolute_dict_list:
            if not creeped_pages.count(i):
                ans_dict_list.append(i)
        return self.get_absolute_dirct(ans_dict_list)

    def get_images(self):
        # download all the images in the image_list
        self.watiing_image_list = self.getImageAbsList()
        # print(self.absoluteRoot + ' images download waiting list === ')
        # print(self.watiing_image_list
        for file_abs in self.watiing_image_list:
            if self.download_image(file_abs[:-1]):
                print('Downloaded >>> ' + file_abs[:-1])
                self.downloaded_images.append(file_abs[:-1])
            else:
                print('Not download >>> ' + file_abs[:-1])
        if len(self.watiing_image_list) == len(self.downloaded_images):
            return True
        else:
            return False

    def run(self):
        print('Current layer: ' + str(self.layer))
        threads = []
        # print(self.parent_html)
        if not self.layer == 0:
            self.layer -= 1
            self.href_list = self.getSrcList()
            # print("Href list: ===\n" + str(self.href_list))
            for sub_domain in self.href_list:
                t = Creeper(sub_domain, self.layer)
                # self.creeped_page.append(sub_domain)
                t.start()
                threads.append(t)
            for thread in threads:
                thread.join()

        if self.get_images():
            print("===\nDownload from {}, is completed!\n===".format(self.absoluteRoot))
        else:
            print("===\nNot Completed from {}!\n==={}\n".format(self.absoluteRoot, len(self.downloaded_images)))


if __name__ == '__main__':
    domain = "http://csse.xjtlu.edu.cn/classes/CSE205/"
    layer = 5
    cont = True
    while cont:
        domain = input("Please input your url: ")
        if domain[:7] == 'http://' or domain[:8] == 'https://':
            cont = False
        else:
            print('IT SHOULD START WITH "http://" or "https://" ')

    cons = True
    while cons:
        layer = input("Please input your crawle layer: (default as 5)")
        try:
            layer = int(layer)
            cons = False
        except Exception as e:
            print('IT SHOULD BE AN "integer"!')

    creeped_pages = []
    thread1 = Creeper(domain, layer)
    thread1.start()
    thread1.join()
    print("creeped_page: ")
    print(creeped_pages)
