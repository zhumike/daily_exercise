# -*- coding: utf-8 -*-
# @Time : 2022/9/28 8:35 下午
# @Author : zhuzhenzhong

# coding:utf-8
from dateutil.relativedelta import relativedelta
import datetime

import time


# 上一个双月：  双月的逻辑将一年12个月分成了六个双月{1-2,3-4,5-6,7-8,9-10,11-12}，数据表中存储双月时间需要存储年份和月份的信息
# 正常来说，双月时间段里第一天的凌晨开始，各个MCN机构的上一个双月中结算金额计算得到的权益等级就应该更新。
# 同时上一个双月的信息（包含机构号，双月的时间，双月的结算金额和机构权益等级）也应该存到一个单独的数据表中。
# 特殊的情况是：如果是1月或者2月，上一个双月就应当是上一年的11~12月
def get_last_bimonth(date=datetime.date.today()):
    """
    函数根据被调用时的时间，获取传入上一个双月时间段的开始时间，返回类型为datetime.date
    当前月份是奇数时，上一个双月的开始月份在两个月前；否则开始月份在三个月之前
    """
    if date.month % 2 == 0:
        last_bi_month = date - relativedelta(months=3)
    else:
        last_bi_month = date - relativedelta(months=2)
    return last_bi_month

time_now = get_last_bimonth()
print(time_now)

# def get_last_bimonth(date=datetime.date.today()):
#     """
#     函数根据被调用时的时间，获取传入上一个双月时间段的开始时间，返回类型为datetime.date
#     当前月份是奇数时，上一个双月的开始月份在两个月前；否则开始月份在三个月之前
#     """
#     if date.month % 2 == 0:
#         last_bi_month = date - relativedelta(months=3)
#     else:
#         last_bi_month = date - relativedelta(months=2)
#     return last_bi_month
#
#
# def get_last_bimonth_string(date=datetime.date.today()):
#     last_bi_month = get_last_bimonth()
#     # datetime.date中的year,month都是int类型,str(date)返回年月日(2022-03-12)
#     # print "%04d-%02d-%02d" % (last_bi_month.year, last_bi_month.month, last_bi_month.month+1)
#     bimonth = "%04d-%02d-%02d" % (last_bi_month.year, last_bi_month.month, last_bi_month.month + 1)
#     return bimonth
#
# time_now = get_last_bimonth_string()
# print(time_now)