# -*- coding: utf-8 -*-
# @Time : 2022/6/30 3:10 下午
# @Author : zhuzhenzhong
a=[
    {
        "code": 190206,
        "name": "烟"
    },
    {
        "code": 190317,
        "name": "膳食营养品"
    },
    {
        "code": 191403,
        "name": "综合类2C电商"
    }
]
a.sort(key=lambda x: x['code'], reverse=True)
print(a)
dict1 = {}
for i in range(len(a)):
    print(a[i])
    dict1.update(a[i])
# print(dict1)
# test_dict = {'test':a}
# print(test_dict)
dic = {'name': 'lee', 'weight': 137, 'age' : 10}
dic1={'age':21,'weight':1.78}
dic.update(dic1)
print(dic)