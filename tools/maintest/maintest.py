# coding=utf-8
# import sys
# sys.path.append("..") #表示导入当前文件的上层目录到搜索路径中
# print(sys.path)
# from folderA import mathtest

# r1= mathtest.maxzhu(4,7)
# print(r1)
def tolist(*args):
    return list(args)

if __name__ == '__main__':
	a=tolist(1,2,'strrrt')
	print(a)