# -*- coding: utf-8 -*-
# @Time : 2022/2/17 3:25 下午
# @Author : zhuzhenzhong

import schedule
from datetime import datetime, timedelta, time

def job():
    print('Boo')

# 每个小时运行作业，18:30后停止
#schedule.every(1).hours.until("18:30").do(job)

# 每个小时运行作业，2030-01-01 18:33 today
#schedule.every(1).hours.until("2030-01-01 18:33").do(job)

# 每个小时运行作业，8个小时后停止
schedule.every(1).hours.until(timedelta(hours=8)).do(job)

# 每个小时运行作业，11:32:42后停止
schedule.every(1).hours.until(time(11, 33, 42)).do(job)

# 每个小时运行作业，2020-5-17 11:36:20后停止
schedule.every(1).hours.until(datetime(2020, 5, 17, 11, 36, 20)).do(job)


schedule.every(10).seconds.until(datetime(2022, 2, 17, 15, 29, 00)).do(job)



while True:
    schedule.run_pending()
    time.sleep(1)