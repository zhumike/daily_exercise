# # -*- coding: utf-8 -*-
# # @Time : 2023/1/17 11:44 上午
# # @Author : zhuzhenzhong
#
# # 比较两个字典部分是否相等
# def compare_two_dict(dict1, dict2, key_list):
#     flag = True
#     keys1 = dict1.keys()
#     print(keys1)
#     keys2 = dict2.keys()
#     print(keys2)
#     if len(key_list) != 0:
#         for key in key_list:
#             if key in keys1 and key in keys2:
#                 if dict1[key] == dict2[key]:
#                     flag = flag & True
#                 else:
#                     flag = flag & False
#             else:
#                 raise Exception('key_list contains error key')
#     else:
#         raise Exception('key_list is null')
#     if flag:
#         result = 'PASS'
#     else:
#         result = 'FAILED'
#     return result
#
#
# if __name__ == '__main__':
#     dict1 = {
#         'a': 1,
#         'b': 2,
#         'c': 3,
#         'd': 4
#     }
#     dict2 = {
#         'a': 1,
#         'b': 2,
#         'c': 3,
#         'd': 8
#     }
#     key_list = ['a', 'c', 'b', 'd']
#     result = compare_two_dict(dict1, dict2, key_list)
#     print(result)
from assertpy import assert_that
#
# key_list = ['a', 'c', 'b', 'd']
# key_list2= ['a', 'c', 'b', 'd']
#
# if key_list==key_list2:
#     print("pass")

dict1 = {
        'a': 1,
        'b': 2,
        'c': 3,
        'd': 4
    }

test_key = dict1.keys()
print(list(test_key))
# print(type(test_key))
