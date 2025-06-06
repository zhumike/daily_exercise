# -*- coding: utf-8 -*-
'''
@Author : zhuzhenzhong
@File : test.py
'''

class Person(object):
    def __init__(self, name, age):
        print("in __init__")
        self._name = name
        self._age = age

p = Person("Wang", 33)
print(p)