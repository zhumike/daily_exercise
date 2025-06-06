# -*- coding: utf-8 -*-
# @Time : 2022/2/17 3:13 下午
# @Author : zhuzhenzhong


import schedule
import time

def greet(name):
    print('Hello {}'.format(name))

# .tag 打标签
schedule.every().day.do(greet, 'Andrea').tag('daily-tasks', 'friend')
schedule.every().hour.do(greet, 'John').tag('hourly-tasks', 'friend')
schedule.every().hour.do(greet, 'Monica').tag('hourly-tasks', 'customer')
schedule.every().day.do(greet, 'Derek').tag('daily-tasks', 'guest')
schedule.every().second.do(greet, 'kitty').tag('second-tasks', 'kity')
schedule.every().second.do(greet, 'Owan').tag('second-tasks', 'Owan')

# get_jobs(标签)：可以获取所有该标签的任务
# friends = schedule.get_jobs()

# 取消所有 daily-tasks 标签的任务
schedule.clear('daily-tasks')
schedule.clear('kity')



while True:
    schedule.run_pending()
    time.sleep(1)