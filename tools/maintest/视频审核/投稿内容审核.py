# -*- coding: utf-8 -*-
# @Time : 2022/6/15 4:11 下午
# @Author : zhuzhenzhong
#!/usr/bin/env python
# encoding: utf-8
"""
@author: taojin
@contact: taojin.20200520@bytedance.com
@file: audit_challenge_item.py
@time: 2022/6/1 下午8:30
"""

try:
    from bytedeventbus.producer.producer import EventbusProducer
    from bytedeventbus.producer.event_builder import EventBuilder
except:
    pass

import sys

sys.path.insert(0, "/opt/tiger/toutiao/app/ad")

from star_common.gateway.base_rpc import challenge_client

def audit_item(item_id, is_pass=1):
    challenge_client.InnerChallengeTcsAuditResultSave(item_id=item_id,
                                                                  tcs_value=1 if is_pass else -1,
                                                                  content_tcs_value=1 if is_pass else -1,
                                                                  relevant_tcs_value=1 if is_pass else -1,
                                                                  anchor_relevant_tcs_value=1,
                                                                  show_reason={})

    challenge_client.InnerSetChallengeItemAudit(item_id=item_id,
                                                                platform_channel=1,
                                                                audit_result_items=[{
                                                                    "audit_type": 3,
                                                                    "audit_value": 1 if is_pass else -1,
                                                                    "audit_source": 'aweme_challenge_audit',
                                                                    "reason": "" if is_pass else '抖音安全初审不通过',
                                                                }])

audit_item(int(sys.argv[1]), int(sys.argv[2]))