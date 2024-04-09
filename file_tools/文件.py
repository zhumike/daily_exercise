# -*- coding: utf-8 -*-
'''
@Author : zhuzhenzhong
@File : 文件.py
'''

with open('zzz.txt', 'r') as f:
    content = f.read()
    print(content)


import os
# 获取当前工作目录
cwd = os.getcwd()
print(cwd)
# 列出目录下的文件和子目录
files = os.listdir('.')
print(files)