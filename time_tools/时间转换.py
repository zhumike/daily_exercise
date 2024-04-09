# -*- coding: utf-8 -*-
'''
@Author : zhuzhenzhong
@File : 时间转换.py
'''

from datetime import datetime
# 时间戳
timestamp = 1650649800
# 将时间戳转换为时间对象
time_obj = datetime.fromtimestamp(timestamp)
# 输出时间对象
print(time_obj)  # 输出结果：2022-12-21 12:30:00
# 将时间对象转换为时间戳
timestamp = int(time_obj.timestamp())
# 输出时间戳
print(timestamp)  # 输出结果：1650649800