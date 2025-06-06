# -*- coding: utf-8 -*-
# @Time : 2022/7/21 3:23 下午
# @Author : zhuzhenzhong
import requests
import json
import datetime

def weather(city):
    url = "http://wthrcdn.etouch.cn/weather_mini?city=%s" % city

    try:
        data = requests.get(url).json()['data']
        city = data['city']
        ganmao = data['ganmao']

        today_weather = data['forecast'][0]
        res = "今天是{}\n今天天气概况\n城市: {:<10}\n时间: {:<10}\n高温: {:<10}\n低温: {:<10}\n风力: {:<10}\n风向: {:<10}\n天气: {:<10}\n\n稍后会发送近期温度趋势图，请注意查看。\
        ".format(
            ganmao,
            city,
            datetime.datetime.now().strftime('%Y-%m-%d'),
            today_weather['high'].split()[1],
            today_weather['low'].split()[1],
            today_weather['fengli'].split('[')[2].split(']')[0],
            today_weather['fengxiang'],today_weather['type'],
        )

        return {"source_data": data, "res": res}
    except Exception as e:
        return str(e)