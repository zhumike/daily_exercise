# -*- coding: utf-8 -*-
'''
@Author : zhuzhenzhong
@File : graphy_test.py
'''
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import pymongo
from bytegraph_gremlin import Client
from bytegraph_gremlin.graph_traversal import new_graph_traversal
from bytegraph_gremlin import ErrorCode
from bytegraph_gremlin.bindings import Int32, Int64, PlaceHolder


# client=pymongo.MongoClient("10.174.255.19", 9827)
# #db = client.star_author
# d1 = client['star_author'] #db
# print(d1)
# jihe = d1['star_author_in_list']
# print(jihe)
# print(jihe.count())





# client = pymongo.MongoClient('mongodb+consul://test4all_w:yzelL2QLRlwt4NtV@toutiao.bytedoc.test4all/test4all')
# db = client.test4all
# collection = db.test_collection
# print('document count is %s' % collection.count_documents({}))

from pymongo import MongoClient

# uri = 'mongodb://host/my_database'
# client = MongoClient(uri)
# db = client.get_default_database()
# print(db.name)


# uri2 = 'mongodb://10.174.255.19:9827/star_author'
# client2 = MongoClient(uri2)
# db2 = client2.get_default_database()
# print(db2.name)

#
# client = pymongo.MongoClient(['10.174.255.19:9827'])
# print(client.get_default_database())



from pymongo import MongoClient
#URI格式见说明文档
#bytedoc psm=toutiao.bytedoc.test_token_likaipeng，是bytedoc psm！！！ 已经见到多个业务填自己服务的psm了
#需要访问的db mongo_press
#sdk回自动通过环境变量拿token，操作前一定要请onccall授权，否则auth失败
#token需要用户环境有token，开发机需要doas生成，tce需要打开服务认证
#开发环境，依赖consul服务，sd lookup bytedoc_psm ，可以验证开发环境是否能发现consul host
#s= "eyJhbGciOiJFUzI1NiIsImtpZCI6IjNpOHhEc2NlR2IwNVhRR2E2aGJSVUdHeVp5Y0xRYVBnIiwidHlwIjoiSldUIn0.eyJhdWQiOlsienRpIl0sImRwYSI6Inp0aSIsImRwciI6InNwaWZmZTovL2JvZS5ieXRlZC5vcmcvbnM6dXNlci9pZDp6aHV6aGVuemhvbmciLCJleHAiOjE2ODU3NjMzMzIsImlhdCI6MTY4NTY3NjkzMiwiaXNzIjoic3ZpZF9wcm92aXNpb25pbmdfc2VydmljZSIsInN1YiI6InNwaWZmZTovL2JvZS5ieXRlZC5vcmcvbnM6dGVzdC9yOmJvZS92ZGM6Ym9lL2lkOmJ5dGVkYW5jZS5ieXRlZG9jLnN0YXJfYXV0aG9yIn0.eYlgDtr7IkJU1JbqKqwi6kTU1hfYt_xaW1iIP6txty1pmCo-yo7e55Mmn5y-wEpbLrwLaLPg9ukCXaZW_-T2mA"
uri = "mongodb+consul+token://bytedance.bytedoc.star_author/star_author?connectTimeoutMS=2000"
#uri = "mongodb+srv://bytedance.bytedoc.star_author/star_author?connectTimeoutMS=2000"
client = MongoClient(uri)
print(client)

db2 = client.get_default_database()
print(db2.name)
# uri = "mongodb+consul+token://bytedance.bytedoc.star_author"
# client = MongoClient(uri)