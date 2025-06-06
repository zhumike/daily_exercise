#!/usr/bin/env python
# encoding: utf-8
import time
import sys
import argparse

sys.path.insert(0, '/opt/tiger/ss_ad/ad_site_env/lib/python2.7/site-packages')
sys.path.insert(0, '/opt/tiger/toutiao/lib')
sys.path.insert(0, '/opt/tiger/toutiao/app/ad')
sys.path.insert(0, '/opt/tiger/toutiao/app/ad/star')
sys.path.insert(0, '/opt/tiger/toutiao/app/ad/star_async')

from kafka_processors.jihe_audit_result_processor import JiheAuditProcessor


def main():
    data = {
        "resource_id": 7010960544953814272,
        "audit_info": {
            "task_id": 0,
            "verify_id": 0,
            "verifier": "zhoufengshun",
            "verify_status": 1,
            "remark": "good",
            'create_time': int(time.time())
        },
        "event_type": "star_material_task_audit",
    }
    JiheAuditProcessor().RealHandler(data)


if __name__ == '__main__':
    main()


