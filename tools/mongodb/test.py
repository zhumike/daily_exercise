# -*- coding: utf-8 -*-
'''
@Author : zhuzhenzhong
@File : test.py
'''

import pymongo
client = pymongo.MongoClient('mongodb+consul://test4all_w:yzelL2QLRlwt4NtV@toutiao.bytedoc.test4all/test4all')
db = client.test4all
collection = db.test_collection
print('document count is %s' % collection.count_documents({}))