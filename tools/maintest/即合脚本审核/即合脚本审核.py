# -*- coding: utf-8 -*-
# @Time : 2021/10/21 8:21 下午
# @Author : zhuzhenzhong

# coding=utf-8

import sys

sys.path.insert(0, '/opt/tiger/toutiao/app/ad/star')
sys.path.append('/opt/tiger/toutiao/app/ad')
sys.path.append('/opt/tiger/toutiao/app/ad/star_async')

from star_async.kafka_processors.jihe_audit_result_processor import JiheAuditProcessor
from star_async.nsq_processors.customer_create_processor import CustomerCreateProcessor


def test():
    import time
    data = {
        "resource_id": 7021485730677391397,
        "audit_info": {
            "task_id": 1223112,
            "verify_id": 332112,
            "verifier": "zhoufengshun",
            "verify_status": 1,
            "remark": "good",
            'create_time': int(time.time())
        },
        "event_type": "star_material_task_audit",
    }
    JiheAuditProcessor().RealHandler(data)

#kafka_processors/jihe_audit_result_processor.py
#新建的文件得在 /opt/tiger/toutiao/app/ad/star_async 这个路径下
#我没把 /opt/tiger/toutiao/app/ad/star_async 这个路径塞到sys.path