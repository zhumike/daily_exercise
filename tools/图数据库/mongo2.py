# -*- coding: utf-8 -*-
'''
@Author : zhuzhenzhong
@File : mongo2.py
'''

# from pymongo import MongoClient
#
# uri = "mongodb+consul+token://bytedance.bytedoc.star_author/star_author"
# client = MongoClient(uri)
# coll = client["star_author"]["test"]
#
# # insert
# data = coll.insert_one({"star": "moon"})
#
# # find
# for item in coll.find({"star": "moon"}):
#     print(item)


from mongoengine import *
connect(db="star_author", host="mongodb+consul+token://bytedance.bytedoc.star_author/star_author")

class TestDocument(Document):
    # check document for more info. https://docs.mongoengine.org/guide/defining-documents.html#document-collections
    meta = {
        "collection": "TestCollection",
        "indexes": [{"fields": ("title",), "unique": True}],
        "index_background": True # very important !!!!!!!!!!!!!!!!
    }
    title = StringField(required=True)
    description = StringField(require=True)
    tags = ListField(StringField(), required=False)

if __name__ == "__main__":
    t = TestDocument()
    t.title = "ByteDoc 快速入门"
    t.description = "ByteDoc 是一个文档型NoSQL数据库"
    t.tags = ["DocumentDB","Database","NoSQL"]
    t.save()

    for x in TestDocument.objects():
        print(x)