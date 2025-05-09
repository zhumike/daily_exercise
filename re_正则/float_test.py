# -*- coding: utf-8 -*-
"""
-------------------------------------------------
# @Project  :daily_exercise
# @File     :float_test
# @Date     :2025/5/9 11:59
# @Author   :zhuzhenzhong
# @Software :校验是否为浮点数
-------------------------------------------------
"""
import re


def validate_float(float_str):
    pattern = r'^-?\d+(\.\d+)?$'
    return bool(re.match(pattern, float_str))

if __name__=='__main__':
    print(validate_float('123.66778'))
    print(validate_float('345'))

