# -*- coding: utf-8 -*-
# @Time : 2022/2/17 3:07 下午
# @Author : zhuzhenzhong

import schedule
import time

#传参给调度器

def greet(name):
    print('Hello', name)

# do() 将额外的参数传递给job函数
schedule.every(2).seconds.do(greet, name='Alice')
schedule.every(4).seconds.do(greet, name='Bob')

while True:
    schedule.run_pending()
    time.sleep(1)

all_jobs = schedule.get_jobs()
print(all_jobs)