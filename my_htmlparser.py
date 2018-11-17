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

# if the tag is 'image', this method will return a list containing all image src address(relatively)
# if nothing happen, return a empty list
def findSrc(tag, htmlText):
    if tag == 'img':
        tagList = findAll('img', htmlText)
    elif tag == 'a':
        tagList = findAll('a', htmlText)
    else:
        return []

    result = []

    if len(tagList) == 0:
        return # 如果毛都没发现 退出
    else:
        # 对于返回的标签列表， 对每个标签进行匹配，找出src部分
        for tag in tagList:
            if len(tag) == 0:
                continue

            if pattern.findall(tag):
                # 找到src, 并写入result
                for src in pattern.findall(tag):
                    srcPattern = re.compile('".*"')
                    src = srcPattern.findall(src) # 将图片地址提取出来
                    src = ''.join(src) # 变成字符串（实在不想学正则表达式 所以写的这么繁琐
                    src = src.strip('"') # 将字符串前后的引号去掉
                    result.append(src) # 加进result
            else:
                continue

    return result # ['imgAddress1', 'imageAddress2']

if __name__ == '__main__':
    file = open('csse.txt', 'rb')

    for i in findAll('img', file.read().decode()):
        print(i)

    file.close()

