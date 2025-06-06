# -*- coding: utf-8 -*-
# @Time : 2022/2/17 3:38 下午
# @Author : zhuzhenzhong
import threading
import time
import schedule

def job1():
    print("I'm running on thread %s \n" % threading.current_thread())
def job2():
    print("I'm running on thread %s \n" % threading.current_thread())
def job3():
    print("I'm running on thread %s  \n" % threading.current_thread())

def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

schedule.every(5).seconds.do(run_threaded, job1)
schedule.every(5).seconds.do(run_threaded, job2)
schedule.every(5).seconds.do(run_threaded, job3)

while True:
    schedule.run_pending()
    time.sleep(1)