# -*- coding: utf-8 -*-
# @Time : 2022/2/17 3:35 下午
# @Author : zhuzhenzhong

from schedule import every, repeat, run_pending
import time

# 此装饰器效果等同于 schedule.every(10).minutes.do(job)
@repeat(every(10).minutes)
def job():
    print("I am a scheduled job")

while True:
    run_pending()
    time.sleep(1)