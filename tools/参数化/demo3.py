# -*- coding: utf-8 -*-
# @Time : 2022/7/21 3:00 下午
# @Author : zhuzhenzhong
from getopt import getopt
import sys

# 获取参数
# sys.argv[1:]：获取除脚本文件名外的所有命令行参数
# opts：存有所有选项及其输入值的元组列表
# args：去除有用的输入以后剩余的部分
opts, args = getopt(sys.argv[1:], 'i:u:p:d:', ['ip=', 'user=', 'pwd=', 'db='])
print(opts)
# 获取参数值
# 短参数
# python3 4_getopt.py -i 127.0.0.1 -u root -p 123456 -d mysqldb
# 长参数
# python3 4_getopt.py --ip 127.0.0.1 -u root -p 123456 -d mysqldb
ip_pre = [item[1] for item in opts if item[0] in ('-i', '--ip')]
ip = ip_pre[0] if len(ip_pre) > 0 else None
print("参数ip：", ip)

user_pre = [item[1] for item in opts if item[0] in ('-u', '--user')]
user = user_pre[0] if len(user_pre) > 0 else None
print("参数user：", user)

pwd_pre = [item[1] for item in opts if item[0] in ('-p', '--pwd')]
pwd = pwd_pre[0] if len(pwd_pre) > 0 else None
print("参数pwd：", pwd)

db_pre = [item[1] for item in opts if item[0] in ('-d', '--db')]
db = db_pre[0] if len(db_pre) > 0 else None
print("参数db：", db)