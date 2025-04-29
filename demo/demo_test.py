# -*- coding: utf-8 -*-
"""
-------------------------------------------------
# @Project  :daily_exercise
# @File     :demo_test
# @Date     :2025/4/29 08:56
# @Author   :zhuzhenzhong
# @Software :PyCharm
-------------------------------------------------
"""

# nums = [1,3,2,2,3,1]
# print(nums[::2])
# print(nums[1::2])
# print(nums[:3][::-1])
# print(nums[3:][::-1])

num1 = [3, 4, 5]
k1 = 3
num2 = [1, 9, 22, 34]
k2 = 4
num1[k1:k1+k2] = num2[:k2]
num1.sort()
print((num1))