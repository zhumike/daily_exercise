# -*- coding: utf-8 -*-
'''
@Author : zhuzhenzhong
@File : mongodbtest.py
'''
from pymongo import MongoClient
uri = "mongodb+consul+token://bytedance.bytedoc.star_author/star_author?connectTimeoutMS=2000"
#uri = "mongodb+srv://bytedance.bytedoc.star_author/star_author?connectTimeoutMS=2000"
client = MongoClient(uri)
db2 = client.get_default_database()
author_list = db2['star_author_in_list']
data = author_list.insert_one({"star": "moon"})

author_list = db2['star_author_in_list']
data = author_list.insert_one({"star": "moon"})

# print(author_list.name)
# print(author_list.full_name)
# result=author_list.find().limit(10)

