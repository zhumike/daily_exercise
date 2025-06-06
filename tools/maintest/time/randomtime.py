# -*- coding: utf-8 -*-
# @Time : 2021/9/26 7:22 下午
# @Author : zhuzhenzhong
import time ,datetime
import time
import datetime
today = datetime.date.today()
print (datetime.datetime.now())
now = time.time() #返回float数据
print(now)
print(type(now))
#  获取当前时间戳---豪秒级级
print(str(int(now)*1000))
print("QATEST"+str(int(now)))
# print(str(int(now)))
#
# today = datetime.date.today()
# trigger_time = datetime.date.fromordinal(today.toordinal() + 0).strftime("%Y-%m-%d %H:%M:%S")
# print(trigger_time)

#new = int(time.mktime(time.strptime(trigger_time, "%Y-%m-%d %H:%M:%S")))

import datetime
# dtime = datetime.datetime.now()
# un_time = time.mktime(dtime.timetuple())
#
t=datetime.datetime.now()
#当前日期
d1 =t.strftime('%Y-%m-%d %H:%M:%S')
print(str(d1))
# #180天后
# # d2=(t+datetime.timedelta(days=180)).strftime("%Y-%m-%d %H:%M:%S")
#
# d2=(t+datetime.timedelta(days=180))
# un_time = time.mktime(d2.timetuple())
# print(int(un_time*1000)) #转为linux时间戳

# import datetime
#
#
# dtime = datetime.datetime.now()
# un_time = time.mktime(dtime.timetuple())
#
# t=datetime.datetime.now()
# d2=(t+datetime.timedelta(days=180))
# un_time = time.mktime(d2.timetuple()) #180天后的linux时间戳，毫秒级别
# print(int(un_time*1000))