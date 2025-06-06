# -*- coding: utf-8 -*-
'''
@Author : zhuzhenzhong
@File : test2.py
'''
from mongoengine import *
connect(db="test4all", host="mongodb+consul+token://toutiao.bytedoc.test4all/test4all")

class TestDocument(Document):
    # check document for more info. https://docs.mongoengine.org/guide/defining-documents.html#document-collections
    meta = {
        #'collection': 'TestEmailShouldBeInThisCollection',
        #'indexes': [{'fields': ('title',), 'unique': True}]
    }
    title = StringField(required=True)
    description = StringField(require=True)
    tags = ListField(StringField(), required=False)

if __name__ == '__main__':
    t = TestDocument()
    t.title = "ByteDoc 快速入门"
    t.description = "ByteDoc 是一个文档型NoSQL数据库"
    t.tags = ["DocumentDB","Database","NoSQL"]
    t.save()