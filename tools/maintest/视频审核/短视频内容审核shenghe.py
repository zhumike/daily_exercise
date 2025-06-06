"""
@author: taojin
@contact: taojin.20200520@bytedance.com
@file: audit_resource.py
@time: 2020/8/5 10:28
"""

"""
抖音内容审核回调处理脚本。
调用方式：
    python audit_item.py <item_id> {<pass>}
item_id: 视频id
pass: 是否审核通过，默认通过，要审核不通过传0.

"""

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

from kafka_processors.item_bind_change_processor import ItemBindChangeProcessor
from star.dals.resource import StarResourceDAL
from star.dals.order import StarOrderDAL, StarChallengeOrderDAL


def main(args):
    item_id = args['item_id']
    resource = StarResourceDAL.query_one({'item_id': args['item_id']})
    order_id = resource.order_or_demand_id
    order_info = StarOrderDAL.query_by_id(order_id)
    is_passed = args['is_passed']
    if order_info:
        user_id = order_info.producer_id
        data = {
            "action_type": args['action_type'],  # 1-create； 2-delete ；3 audit
            "item_id": item_id,
            'is_passed': is_passed,
            "event_time": int(time.time()),  # 投稿时的时间戳
            "user_id": user_id,
            "order_id": order_id,
            'star_atlas_channel': 1,
            'audit_suggests': [{'TimeDesc': '视频第3秒', 'PosDesc': '左上角', 'Suggest': '缺少商标', 'BanReason': '测试内容审核不通过'}]
        }
        ItemBindChangeProcessor().RealHandler(data)
    else:
        challenge_order = StarChallengeOrderDAL.query_by_id(order_id)
        user_id = challenge_order.producer_id
        data = {
            "action_type": args['action_type'],  # 1-create； 2-delete ；3 audit
            "item_id": item_id,
            'is_passed': is_passed,
            "event_time": int(time.time()),  # 投稿时的时间戳
            "user_id": user_id,
            "order_id": order_id,
            'star_atlas_channel': 1,
            'audit_suggests': [{'TimeDesc': '视频第3秒', 'PosDesc': '左上角', 'Suggest': '缺少商标', 'BanReason': '测试内容审核不通过'}]
        }
        ItemBindChangeProcessor().RealHandler(data)

def parse():
    parser= argparse.ArgumentParser()
    parser.add_argument('item_id', help='视频item_id')
    parser.add_argument('is_pass', default=1, type=int, help='是否审核通过，默认为1, 0为不通过')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse()
    args = {
        'action_type': 3,
        'item_id': int(args.item_id),
        'is_passed': True if int(args.is_pass) != 0 else False
    }
    main(args)

    # ad.site.star_kafka_async
    #python qashenhe.py  7008733734207966508 1
    #https://cloud-boe.bytedance.net/paas/services/48640?module=cluster