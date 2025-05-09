# -*- coding: utf-8 -*-
'''
@Author : zhuzhenzhong
@File : unit_test.py
'''


import re
text = "Hello, World! 123"
pattern = r"\d+"  # 匹配数字
pattern2 = r"\w+"  # 匹配字母或数字
matches = re.findall(pattern, text)
print(matches)  # 输出: ['123']
matches2 = re.findall(pattern2,text)
print(matches2)#['Hello', 'World', '123']

