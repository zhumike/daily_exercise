# -*- coding: utf-8 -*-
# @Time : 2022/2/17 3:02 下午
# @Author : zhuzhenzhong

import schedule
import time

def job_that_executes_once():
    # 此处编写的任务只会执行一次...
    print("one time a day working")
    return schedule.CancelJob

schedule.every().day.at('15:05:45').do(job_that_executes_once)

while True:
    schedule.run_pending()
    time.sleep(1)