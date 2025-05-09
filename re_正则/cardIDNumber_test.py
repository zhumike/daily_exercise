# -*- coding: utf-8 -*-
"""
-------------------------------------------------
# @Project  :daily_exercise
# @File     :cardIDNumber_test
# @Date     :2025/5/9 09:57
# @Author   :zhuzhenzhong
# @Software :校验身份证号码
-------------------------------------------------
"""
import re

def validate_id_card(id_card):
    pattern = r'(^\d{15}$)|(^\d{17}([0-9]|X)$)'
    return bool(re.match(pattern,id_card))
if __name__=='__main__':
    print(validate_id_card('330802199109125201'))
    print(validate_id_card('443197009125201'))