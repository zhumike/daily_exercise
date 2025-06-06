#  #-*- coding: utf-8 -*-
# import time
# global qastr
# qastr = []
#
# global result
# result = []
# with open('service.txt', 'r') as f:
# 	for line in f.readlines():
# 		#获取接口备注信息
# 		sa=line.split('req')
# 		if len(sa)<=1:
# 			continue
# 		sa=sa[1]
# 		str2 = sa.replace(")", " ")
# 		if str2 == '':
# 			continue
# 		# print(str2.strip())
# 		sa=sa[0]
# 		# print(sa)
# #获取接口信息
# 		sa=line.split(' ')
# 		if len(sa) <=2:
# 			continue
# 		sr = sa[4]
# 		str2 = sr.replace("Resp", "")
# 		if str2 == '//':
# 			continue
# 		# print(str2)
# 		qastr.append(str2)
# print(len(qastr))
#
# for i in qastr:
# 	if i[0] != 'I':
# 		print(i)
# 		result.append(i)
#
# result = result
# file2 = open('result.txt','w')
# for i in result:
# 	file2.write(i+'\n')
# file2.close()
#
#
#
import random
t = random.randint(1,3)
# t = random.sample(range(1, 100000), 201)
print(t)
