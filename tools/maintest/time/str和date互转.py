# -*- coding: utf-8 -*-
# @Time : 2022/3/24 10:54 上午
# @Author : zhuzhenzhong

import datetime
# str转时间格式：
dd = '2022-03-24 00:00:00'
dd = datetime.datetime.strptime(dd, "%Y-%m-%d %H:%M:%S")
print(dd,type(dd))

# 时间格式转str:
dc = dd.strftime("%Y-%m-%d %H:%M:%S")
print(dc,type(dc))

test_dd = '2022-03-24'
dt = datetime.datetime.strptime(test_dd, "%Y-%m-%d")
print(dt,type(dt))
if dt == dd:
    print("pass")