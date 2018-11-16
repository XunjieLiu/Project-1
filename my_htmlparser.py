import re

# This method will return all complete segments with corresponding tag
# Like findAll(img, html) ----> <img src = "blablabla" />
def findAll(tag, htmlText):
	if tag == 'img':
		tag = "<img .*?>" # MD我是天才！
	elif tag == 'a':
		tag = "<a .*</a>{1}"
	else:
		return []

	pattern = re.compile(tag, flags=re.IGNORECASE) # Case insensitive

	result = pattern.findall(htmlText)
	
	if len(result) != 0:
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
		pattern = re.compile('src.*".*?"') # 匹配img标签的src部分

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