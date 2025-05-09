# -*- coding: utf-8 -*-
"""
-------------------------------------------------
# @Project  :daily_exercise
# @File     :name_test
# @Date     :2025/5/9 10:17
# @Author   :zhuzhenzhong
# @Software :校验中英文姓名
-------------------------------------------------
"""
import  re
def validate_name(name):
    pattern = r'[\u4e00-\u9fa5a-zA-Z\s]+$'
    return bool(re.match(pattern,name))

if __name__=='__main__':
    print(validate_name('李四'))
    print(validate_name('王 五 '))
    print(validate_name('张青     '))
    print(validate_name('mike zhu'))



