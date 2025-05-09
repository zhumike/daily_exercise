# -*- coding: utf-8 -*-
"""
-------------------------------------------------
# @Project  :daily_exercise
# @File     :integer_test
# @Date     :2025/5/9 11:56
# @Author   :zhuzhenzhong
# @Software :校验整数
-------------------------------------------------
"""
import re


def validate_integer(integer_str):
    pattern = r'^-?\d+$'
    return bool(re.match(pattern, integer_str))

if __name__=='__main__':
    print(validate_integer('0'))
    print(validate_integer('234'))