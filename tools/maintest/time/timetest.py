# -*- coding: utf-8 -*-
# @Time : 2021/8/16 2:50 下午
# @Author : zhuzhenzhong



import time
import datetime
today = datetime.date.today()
#print (datetime.datetime.now())
now = time.time() #返回float数据
#  获取当前时间戳---豪秒级级
#print(str(int(now)))
# #
# print(today)

#1112598   1642509828
#
trigger_time = datetime.date.fromordinal(today.toordinal() + 3).strftime("%Y-%m-%d %H:%M:%S")
print(trigger_time)

trigger_time2 = datetime.date.fromordinal(today.toordinal() -30).strftime("%Y-%m-%d %H:%M:%S")
print(trigger_time2)

trigger_time2 = int(time.mktime(time.strptime(trigger_time2, "%Y-%m-%d %H:%M:%S")))
print(str(trigger_time2))

#print(type(trigger_time))
# t1=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
# print(str(t1))
# # # #
# # #
# # # dt = '2020-04-02 13:58:51'
#ts = int(time.mktime(time.strptime(trigger_time, "%Y-%m-%d %H:%M:%S")))
#print(ts)
# # #
# # print(datetime.datetime.now())
#
# # today = datetime.date.today()
# trigger_time = datetime.date.fromordinal(today.toordinal() + 30).strftime("%Y-%m-%d %H:%M:%S")
# # trigger_time = str(int(time.mktime(time.strptime(trigger_time, "%Y-%m-%d %H:%M:%S")))*1000)
# print(str(trigger_time))


# a1=int((datetime.datetime.now() + datetime.timedelta(days=900)).timestamp())
# print(a1)