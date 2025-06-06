# -*- coding: utf-8 -*-
# @Time : 2022/8/3 4:58 下午
# @Author : zhuzhenzhong
# 简单的dict
lst = [('d', 2), ('a', 4), ('b', 3), ('c', 2)]

# 按照value排序
lst.sort(key=lambda k: k[1])
print(lst)

# 按照key排序
lst.sort(key=lambda k: k[0])
print(lst)
#https://ai.52learn.online/133