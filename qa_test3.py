# -*- coding: utf-8 -*-
"""
-------------------------------------------------
# @Project  :daily_exercise
# @File     :qa_test3
# @Date     :2025/5/21 15:38
# @Author   :zhuzhenzhong
# @Software :PyCharm
输入[3,0,1]  输出2
[1,2，3，4，5，6，8]   输出7
-------------------------------------------------
"""

def find_missing_number(start:int,nums:list)-> int:
    n=len(nums)
    full_sum  = (start+start+n)*(n+1)//2
    sum1 = 0
    for i in range(start,start+n+1):
        sum1+=i
    return sum1 - sum(nums)

if __name__=="__main__":
    num_list = [1,2,3,4,5,6,8]
    print(find_missing_number(1,num_list))









