# -*- coding: utf-8 -*-
# @Time : 2022/7/21 3:28 下午
# @Author : zhuzhenzhong

import matplotlib.pyplot as plt
import re
import datetime


def Future_weather_states(forecast, save_path, day_num=5):
    '''
    展示未来的天气预报趋势图
    :param forecast: 天气预报预测的数据
    :param day_num: 未来几天
    :return: 趋势图
    '''
    future_forecast = forecast
    dict = {}

    for i in range(day_num):
        data = []
        date = future_forecast[i]["date"]
        date = int(re.findall("\d+", date)[0])
        data.append(int(re.findall("\d+", future_forecast[i]["high"])[0]))
        data.append(int(re.findall("\d+", future_forecast[i]["low"])[0]))
        data.append(future_forecast[i]["type"])
        dict[date] = data

    data_list = sorted(dict.items())
    date = []
    high_temperature = []
    low_temperature = []
    for each in data_list:
        date.append(each[0])
        high_temperature.append(each[1][0])
        low_temperature.append(each[1][1])
        fig = plt.plot(date, high_temperature, "r", date, low_temperature, "b")

    current_date = datetime.datetime.now().strftime('%Y-%m')
    plt.rcParams['font.sans-serif'] = ['Tahoma']
    plt.rcParams['axes.unicode_minus'] = False
    plt.xlabel(current_date)
    plt.ylabel("℃")
    plt.legend(["高温", "低温"])
    plt.xticks(date)
    plt.title("最近几天温度变化趋势")
    plt.savefig(save_path)