# -*- coding: utf-8 -*-
'''
@Author : zhuzhenzhong
@File : unit_test.py
'''

from id_validator import validator
# 生成10个符合规范的身份证号码
for i in range(10):
    id_card = validator.create_id_card()
    print(id_card)