# -*- coding: utf-8 -*-
# @Time : 2021/9/28 6:45 下午
# @Author : zhuzhenzhong
from assertpy import assert_that
strtest = "[1, 4, 6, 52, 57, 103]"
print(strtest)

listtest=[1, 4, 6, 52, 57, 103]
listtest = str(listtest)
print(listtest)

if assert_that(strtest).is_equal_to(listtest):
    print("pass")