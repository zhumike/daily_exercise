# -*- coding: utf-8 -*-
"""
-------------------------------------------------
# @Project  :daily_exercise
# @File     :qa_0709
# @Date     :2025/7/9 16:36
# @Author   :zhuzhenzhong
# @Description :一个nxn的行列均升序的二维矩阵，请从其中找到数值第k小的数，并返回。
-------------------------------------------------
"""
import heapq

class Solution:
    def search(self,nlist,k):
        n=len(nlist)
        heap = [(nlist[i][0],i,0) for i in range(n) ]
        heapq.heapify(heap)
        print(heap)

        for _ in range(k):
            val,row,col = heapq.heappop(heap)
            print(val,row,col)

            if col<n-1:
                heapq.heappush(heap,(nlist[row][col+1],row,col+1))


        return val


if __name__=="__main__":

    test_case = [[1, 2, 3],[1, 2, 4],[2, 3, 6]]
    num = 2
    demo =Solution()

    print(demo.search(test_case,num))



