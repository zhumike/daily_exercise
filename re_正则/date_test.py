# -*- coding: utf-8 -*-
"""
-------------------------------------------------
# @Project  :daily_exercise
# @File     :date_test
# @Date     :2025/5/9 10:50
# @Author   :zhuzhenzhong
# @Software :日期校验
-------------------------------------------------
"""

import re
import datetime

def validate_date(date):
    pattern = r'\d{4}-\d{2}-\d{2}$'
    if re.match(pattern, date):
        try:
            datetime.datetime.strptime(date, '%Y-%m-%d')
            return True
        except ValueError:
            return False
    else:
        return False

if __name__=='__main__':
    print(validate_date('2025-09-10'))
    print(validate_date('2025-09-1'))
    print(validate_date('2025-09-10 32:43'))
