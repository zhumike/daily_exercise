# -*- coding: utf-8 -*-
"""
-------------------------------------------------
# @Project  :daily_exercise
# @File     :password_test
# @Date     :2025/5/9 11:03
# @Author   :zhuzhenzhong
# @Software :密码强度校验，至少包含一个大写字母、一个小写字母、一个数字和一个特殊字符
-------------------------------------------------
"""
import re


def validate_password(password):
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    return bool(re.match(pattern, password))

if __name__=='__main__':
    print(validate_password('dk@1P2222'))

