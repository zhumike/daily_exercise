# -*- coding: utf-8 -*-
"""
-------------------------------------------------
# @Project  :daily_exercise
# @File     :post_code_test
# @Date     :2025/5/9 12:01
# @Author   :zhuzhenzhong
# @Software :校验邮编
-------------------------------------------------
"""

import re

def validate_postal_code(postal_code):
    pattern = r'^\d{6}$'
    return bool(re.match(pattern, postal_code))

if __name__=='__main__':
    print(validate_postal_code('345678'))

