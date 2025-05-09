# -*- coding: utf-8 -*-
"""
-------------------------------------------------
# @Project  :daily_exercise
# @File     :phoneNumber_test
# @Date     :2025/5/9 09:45
# @Author   :zhuzhenzhong
# @Software :校验手机号
-------------------------------------------------
"""
import re
def validate_phone_number(phone:str):
    pattern = r'^1[3-9]\d{9}$'
    return bool(re.match(pattern,phone))
if __name__=='__main__':
    testStr = '13456890921'
    testStr2 = '13r56890921'
    testNum = 23
    print(validate_phone_number(testStr))
    print(validate_phone_number(testStr2))
    # print(validate_phone_number(testNum))