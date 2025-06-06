# -*- coding: utf-8 -*-
# @Time : 2022/11/17 11:47 上午
# @Author : zhuzhenzhong
import re
pattern = re.compile(r'(13\d|14[579]|15[^4\D]|17[^49\D]|18\d)\d{8}')
str1 = '13609857834'
print(pattern.search(str1).group())