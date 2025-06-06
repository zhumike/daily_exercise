# -*- coding: utf-8 -*-
# @Time : 2022/10/25 11:15 上午
# @Author : zhuzhenzhong

role_list= [
    {
        "role_desc": "开发用的",
        "role_name": "开发人员查看",
        "industry_ids": [
            {
                "industry_id": "20001",
                "industry_name": "DIY电脑"
            }
        ],
        "ref_user_count": "0",
        "role_id": "62"
    },
    {
        "role_desc": "qa",
        "role_name": "测试",
        "industry_ids": [
            {
                "industry_id": "20001",
                "industry_name": "DIY电脑"
            }
        ],
        "ref_user_count": "0",
        "role_id": "60"
    },
    {
        "role_desc": "开发用的",
        "role_name": "开发人员查看",
        "industry_ids": [
            {
                "industry_id": "20004",
                "industry_name": "茶"
            }
        ],
        "ref_user_count": "0",
        "role_id": "62"
    }
]

print(role_list)
print(len(role_list))
l1 = [ _.get('role_id') for _ in role_list]
print(l1)
# set_List = set(role_list)
# print(set_List)
#
# if len(role_list)!=len(set_List):
#     print("有重复元素")