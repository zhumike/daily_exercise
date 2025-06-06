# -*- coding: utf-8 -*-
# @Time : 2022/7/21 2:53 下午
# @Author : zhuzhenzhong
import argparse

# 构建一个命令行参数解析对象
parser = argparse.ArgumentParser(description='命令行参数')

# 设置3个参数
# 参数1：arg1，整型，非必须传入参数
# 参数2：arg2，字符串，非必须传入参数，包含默认值「xag」
# 参数3：arg3，字符串类型，必须传入的参数
parser.add_argument('--arg1', '-a1', type=int, help='参数1，非必须参数')
parser.add_argument('--arg2', '-a2', type=str, help='参数2，非必须参数,包含默认值', default='xag')
parser.add_argument('--arg3', '-a3', type=str, help='参数3，必须参数', required=True)

# 解析参数,获取所有的命令行参数（Namespace），然后转为字典
args = vars(parser.parse_args())

# 获取所有参数
print("所有命令行参数为:")
for key in args:
    print(f"命令行参数名:{key}，参数值:{args[key]}")