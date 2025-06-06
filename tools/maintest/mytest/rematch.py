# -*- coding: utf-8 -*-
# @Time : 2021/8/24 8:18 下午
# @Author : zhuzhenzhong
#https://www.cnblogs.com/ddzj01/p/10927054.html
# coding=utf-8
import re
"""正则表达式
"""
s = ['abc-123-cba',       #'abc'在最前面
    '123-abc-aabbcc-123', #'abc'在中间
    'a-2-3-b-1',          #最前面是'a'
    'b-x-c-a-1',          #最前面是'b'
    'z-a-1',              #'a'在中间
    'x-y-z',              #字符串没有任何'a','b','c'
    'cbaabc',              #字符串全是'a','b','c'组成
     'abc'
]

#字符串中有'abc'就匹配成功
# st = r'abc'
# for i in s:
#     m = re.search(st, i)
#     if m:
#         print(i)

#字符串中只要有'a'或'b'或'c'，就匹配出来
# st = r'[abc]'
# for i in s:
#     m = re.search(st, i)
#     if m:
#         print(i)

#字符串中只有'abc'开头的才匹配出来
# st = r'^abc'
# for i in s:
#     m = re.search(st, i)
#     if m:
#         print(i)

#字符串由'a'或'b'或'c'开头的都匹配出来了
# st =  '^[abc]'
# for i in s:
#     m = re.search(st, i)
#     if m:
#         print(i)

#字符串只要有除'a'和'b'和'c'的字符就都匹配出来了
st =   '[^abc]'
for i in s:
    m = re.search(st, i)
    if m:
        print(i)