import re

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
        for src in result:
            print(src)
            temp = src.split('"')[1]
            src = temp
            if src[0] == '/':
                src = src[1:]
            print(src)
        '''
        '''
        返回的src可能是这样的：/en/assets/image-cache/templates/xjtlu/img/hero-image-default-1.9cdb9aa2.jpg
        也可能是这样的：testImages/upside-down-cat-thumbnail.jpg
        我们只接受第二种，所以需要对第一种进行操作
        '''
        return result
    else:
        return []

if __name__ == '__main__':
    file = open('csse.txt', 'rb')

    for i in findAll('img', file.read().decode()):
        print(i)

    file.close()

