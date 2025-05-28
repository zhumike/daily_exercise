# -*- coding: utf-8 -*-
"""
-------------------------------------------------
# @Project  :daily_exercise
# @File     :qa_test2
# @Date     :2025/5/15 16:00
# @Author   :zhuzhenzhong
# @Software :PyCharm

字符串压缩
实现一个方法，将重复字符的连续出现次数用数字表示，并将其压缩到一个新的字符串中。如果压缩后的字符串长度不小于原字符串，则返回原字符串。
输入: "aabcccccaaa"
输出: "a2b1c5a3"
输入: "abcdef"
输出: "abcdef" (由于压缩后没有变短)
-------------------------------------------------
"""

def demo_test(s:str)->str:
    if len(s)<=1:
        return s
    new_compressed = []#压缩的子串
    current_str = s[0]
    count = 1

    for char in s[1:]:
        if char == current_str:
            count+=1
        else:
            new_compressed.append(f"{current_str}{count if count>1 else 1}")
            current_str = char
            count =1
    new_compressed.append(f"{current_str}{count if count>1 else 1}")
    expect_str = "".join(new_compressed)
    return expect_str if len(new_compressed) < len(s) else s

demo_str1 = "abbddf"
demo_str2 = "abcdef"
print(demo_test(demo_str1),demo_test(demo_str2))



