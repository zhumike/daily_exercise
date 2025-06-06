# -*- coding: utf-8 -*-
# @Time : 2022/2/17 3:44 下午
# @Author : zhuzhenzhong

import schedule
import logging
import time

logging.basicConfig()
schedule_logger = logging.getLogger('schedule')
# 日志级别为DEBUG
schedule_logger.setLevel(level=logging.INFO)

def job():
    print("Hello, Logs")

schedule.every().second.do(job)

schedule.run_all()
#schedule.clear()

while True:
    schedule.run_pending()
    time.sleep(1)