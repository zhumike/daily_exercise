# -*- coding: utf-8 -*-
'''
@Author : zhuzhenzhong
@File : data_generate2.py
数据自动化生成
'''


import requests
import re
import random
import time
import csv
import os
from faker import Faker
fake = Faker(locale="zh_CN")

"""
生成指定要求的身份证等数据信息
"""


def generate_id(birthyear,age,region='110102'):
    """
    生成身份证号码
    :param region:
    :param birthyear:
    :param age:
    :return:
    """
    # region = "110110"
    birthday = str(year(birthyear,age))+str(month())+str(getDay(year(birthyear,age),month()))
    sex = random.randint(1,2)
    # 顺序码2位数
    sxm = str(random.randint(10,99))
    id_number = str(region) + str(birthday) + str(sxm) + str(sex)
    # print("身份证前17位 %s " % id_number)
    # 生成校验码，最后一位校验码生成规则
    factor = [7,9,10,5,8,4,2,1,6,3,7,9,10,5,8,4,2]
    verify_codes = "10X98765432"
    check_sum = 0
    for i in range(17):
        check_sum += int(id_number[i]) * factor[i]
    verify_code = verify_codes[check_sum % 11]
    # print("校验码 %s " % verify_code)
    id_number = id_number + verify_code
    # print("最终身份证号码 %s " % id_number)
    return id_number,birthday,sex


def year(birthyear,age):
    """
    生成年份
    :param year:从哪一年开始
    :param age: 小于几岁的年份
    :return: 从1985开始算，row-18（age)直接过滤掉小于18(age)岁出生的年份
    """
    now = time.strftime('%Y')
    YY = random.randint(int(birthyear), int(now)-int(age))
    return YY

def month():
    """
    生成月份
    :return: zfill(）返回指定长度的字符串，原字符串右对齐，前面填充0
    """
    three = str(random.randint(1, 12))
    mon = three.zfill(2)
    return mon

def getDay(year, month):
    """
    根据传来的年月份返回日期
    :param year:
    :param month: 1、3、5、7、8、10、12为31天，4、6、9、11为30天，2月闰年28天，其余29天
    :return:
    """
    aday = 0
    if month in (1, 3, 5, 7, 8, 10, 12):
        aday = random.randint(1, 31)
    elif month in (4, 6, 9, 11):
        aday = random.randint(1, 30)
    else:
        if ((year % 4 == 0 and year % 100 !=0) or (year % 400 == 0)):
            aday = random.randint(1, 28)
        else:
            aday = random.randint(1, 29)
    dd = str(aday).zfill(2)
    return dd

def getPhone(start_num='180'):
    """
    随机生成手机号
    :return:
    """
    # start_nums  = [
    #     '134','135','136','137','138','139','147','150','151','152','157','158','159','165','172','178','182','183','184','187','188','198','130','131','132','145','155','156','166','171','175','176','185','186','133','149','153','173','177','180','181','189','199'
    # ]
    # start_nums = ['180']
    # start_num = random.choice(start_nums)
    num = random.randint(00000000,99999999)
    end_num = str(num).zfill(8)
    phone_num = start_num + str(end_num)
    return phone_num


if __name__ == "__main__":
    file = r'/Users/admin/zhuzhenzhong/code/ad_daily_learning/testdata.csv'
    num = int(input("请输入要生成的用户个数：")) + 1
    birthyear = int(input("请输入从哪一年开始的出生年份："))
    age = int(input("请输入要生成的用户最小年龄："))
    region = str(input("请输入身份证前6位，如110102："))
    start_num = str(input("请输入手机号前3位，如188："))
    with open(file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=('身份证号码', '出生年月日', '手机号', '姓名', '性别'))
        writer.writeheader()
        for row in range(1, num):
            idinfo = generate_id(birthyear,age,region)
            idcard = idinfo[0] + '\t'
            phone_num = getPhone(start_num)
            if idinfo[2] ==1:
                sex = '男'
                name = fake.name_male()
            else:
                sex = '女'
                name = fake.name_female()
            writer.writerow({'身份证号码': idcard, '出生年月日': idinfo[1], '手机号':phone_num, '姓名': name, '性别': sex})