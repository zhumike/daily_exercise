# -*- coding: utf-8 -*-
# @Time : 2021/6/23 4:45 下午
# @Author : zhuzhenzhong
qa =[
        {
            "type_tag": "全部",
            "type_code": ""
        },
        {
            "type_tag": "美食",
            "type_code": "010000"
        },
    ]

# qa = str(qa)
# print(qa)
# print(type(qa))
# # print(qa)
for i in qa:
    # print(i)
    if '美食' in str(i):
        print("ok")

# def response_has(str_one,str_two):#判断str_two是否包含于str_one
#     flag = None
#     try:
#         if isinstance(str_one,list):
#             for i in str_one:
#                if  str_two in i:
#                   flag = True
#         else:
#             if str_two in str_one:
#                 flag = True
#     except:
#         print('fail!')
#         flag = False
#     return flag
# q=response_has(qa,'美食')
# print(q)

