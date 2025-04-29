# -*- coding: utf-8 -*-
"""
-------------------------------------------------
# @Project  :daily_exercise
# @File     :compare_test
# @Date     :2025/4/28 18:53
# @Author   :zhuzhenzhong
# @Software :PyCharm
-------------------------------------------------
"""
#比较ascii值
def  compare(a,b):
    return str(a) + str(b) > str(b) + str(a)

t1 = 4
t2 = 5

print(compare(4,5))
