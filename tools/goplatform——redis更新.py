# -*- coding: utf-8 -*-
# @Time : 2023/1/16 5:40 下午
# @Author : zhuzhenzhong
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import json
import sys

sys.path.insert(0, '/opt/tiger/ss_ad/ad_site_env/lib/python2.7/site-packages')
sys.path.insert(0, '/opt/tiger/')
sys.path.insert(0, '/opt/tiger/toutiao/app/ad')
sys.path.insert(0, '/opt/tiger/toutiao/webarch_lib')
sys.path.insert(0, '/opt/tiger/toutiao/app/ad/star_platform')

from star_common.storage.redis_star_platform_init import redis_star_platform_cli
redis_client = redis_star_platform_cli

if __name__ == "__main__":
    redis_key = "7020021033155546383_7173876835187425316"
    redis_value = {"item_id": 7020021033155546383,
                   "fail_reason": "",
                   "audit_status": 1,
                   "industry_anchor_id": 7173876835187425316}
    redis_client.set(redis_key, json.dumps(redis_value), ex=1 * 3600 * 24 * 60)  # 保存2个月