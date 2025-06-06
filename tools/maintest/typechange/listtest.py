# -*- coding: utf-8 -*-
# @Time : 2021/10/19 11:05 上午
# @Author : zhuzhenzhong
strtest = "[1, 4, 52, 103, 57, 6]"
print(strtest)
print(type(strtest))

qa1 = eval(strtest)
print(type(qa1))
qa1.sort()
print(qa1)