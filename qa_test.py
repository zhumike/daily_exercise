# -*- coding: utf-8 -*-
"""
-------------------------------------------------
# @Project  :daily_exercise
# @File     :qa_test
# @Date     :2025/5/15 15:40
# @Author   :zhuzhenzhong
# @Software :PyCharm
-------------------------------------------------
"""

def demo_test(s:str)-> int:
    char_index ={}
    left = 0
    sub_max_length = 0#最大不重复子串长度
    for right, char in enumerate(s):
        if char in char_index and char_index[char] >= left:
            left = char_index[char]+1
        char_index[char] = right #更新位置
        sub_max_length = max(sub_max_length,right-left+1)

    return sub_max_length

demo_str = "abcccccc"
demo_str2 = "abcdefrg"
demo_str3 = "abcdefrg"
demo_str4 = ""

print(demo_test(demo_str4))


