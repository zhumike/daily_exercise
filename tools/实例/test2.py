# -*- coding: utf-8 -*-
'''
@Author : zhuzhenzhong
@File : test2.py
'''

class LabelType:
    author_info_label = 4
    encourage_projects_label = 8
    category_label = 9
    douyin_industry_label = 101
    toutiao_content_label_v2 = 105
    live_content_label = 3
    industry_label = 2
    toutiao_content_label = 5
    xigua_content_label = 6
    huoshan_content_label = 7
    content_label = 1

qa =  LabelType()


for attr in dir(qa):
    print(attr)