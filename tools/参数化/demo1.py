# -*- coding: utf-8 -*-
# @Time : 2022/7/21 2:51 下午
# @Author : zhuzhenzhong
import sys

if __name__ == '__main__':
    # 获取参数列表
    # 注意：sys.argv[0] 代表第一个参数，即：脚本名称「1_sys.argv.py」
    # 其他参数列表
    args = sys.argv[1:]

    # 参数个数
    args_length = len(sys.argv) if sys.argv else 0

    print("排除运行主文件参数，其他参数列表为:", args)

    print("参数总数：", args_length)
