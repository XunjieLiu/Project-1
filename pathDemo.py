import os

# current file dir = D:\Study\Year 3\CSE205\Project 1

url = 'http://csse.xjtlu.edu.cn/classes/CSE205/testImages/upside-down-cat-thumbnail.jpg'

def getPath(url):
	result = url.split('/', 3) # 利用split，把文件路径分割出来
	path = result[3]

	return path

def creatFolder(path):
	names = []

	for i in path.split('/'):
		if i != '' and i != 'http:':
			names.append(i)
	# names = ['csse.xjtlu.edu.cn', 'classes', 'CSE205', 'testImages', 'upside-down-cat-thumbnail.jpg']
	

	'''
	currentPath = os.getcwd()

	for name in names:
		if name != '':
			if os.path.exists(name):
				print("File exists")
			else:
				os.mkdir(name)
				
			currentPath = currentPath + '\\' + name
			os.chdir(currentPath)

	return currentPath
	'''

creatFolder(url)