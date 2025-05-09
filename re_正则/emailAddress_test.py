# -*- coding: utf-8 -*-
"""
-------------------------------------------------
# @Project  :daily_exercise
# @File     :emailAddress_test
# @Date     :2025/5/9 10:42
# @Author   :zhuzhenzhong
# @Software :校验邮箱地址
-------------------------------------------------
"""
import re

def validate_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(pattern, email))

if __name__=='__main__':
    print(validate_email('zzz12+3-123@example.com'))  #
