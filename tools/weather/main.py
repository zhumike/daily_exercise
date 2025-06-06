# -*- coding: utf-8 -*-
# @Time : 2022/7/21 3:23 下午
# @Author : zhuzhenzhong
import tianqi
import qushi
import os

# 天气预报趋势图保存路径
_path = os.path.dirname(os.path.abspath(__file__))
save_path = os.path.join(_path ,'./tmp/weather_forecast.jpg')
# 获取天气预报信息
content = tianqi.weather("上海")
print(content)
#
#
qushi.Future_weather_states(content['source_data']['forecast'], save_path)