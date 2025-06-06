# -*- coding: utf-8 -*-
# @Time : 2021/12/29 5:42 下午
# @Author : zhuzhenzhong
# coding=utf-8

try:
    from typing import List, Tuple, Dict
except ImportError:
    pass

import datetime
import os
os.environ['SERVICE_MESH_EGRESS_ADDR'] = '/opt/tiger/toutiao/var/service/%s.mesh/rpc.egress.sock' % os.getenv('TCE_PSM')
import sys
sys.path.insert(0, '/opt/tiger/ss_ad/ad_site_env/lib/python2.7/site-packages')
sys.path.insert(0, '/opt/tiger/toutiao/lib')
sys.path.insert(0, '/opt/tiger/toutiao/app/ad')
sys.path.insert(0, '/opt/tiger/toutiao/app/ad/star_author')


from star_author.dals.author_creative import StarCreativeFeedbackInfoDAL
from star_core.config.base import IS_DEV, IS_BOE
from star_core.data.tqs_client import query_with_tqs_and_fetch_result
from star_common.utils.util import split_list
from star_common.utils.converter import datetime2string


class Feedback(object):
    def __init__(self, star_id, user_role, order_id, spu_id, feedback_level, feedback_info, feedback_time):
        self.star_id= star_id
        self.user_role = user_role
        self.order_id = order_id
        self.spu_id = spu_id
        self.feedback_level = feedback_level
        self.feedback_info = feedback_info
        self.feedback_time = feedback_time


def query_stat_from_hive():
    # type: () -> Dict
    """
    获取创意定制反馈信息
    """
    if IS_DEV or IS_BOE:
        return {}
    date_str = datetime2string(datetime.datetime.now() - datetime.timedelta(days=1), format='%Y%m%d')
    hive_sql = '''
        select 
            star_id,
            user_role,
            order_id,
            spu_id,
            feedback_level,
            feedback_info,
            feedback_time
        from 
            ad_star.star_creative_feedback_info
        where 
            date='%s'
    ''' % date_str
    rows = query_with_tqs_and_fetch_result(hive_sql)
    if not rows or len(rows) <= 1:
        print 'empty rows: ', rows
        return {}

    return {int(_[2]): Feedback(*_) for _ in rows[1:]}


def process():
    feedback_dict = query_stat_from_hive()
    _order_ids = feedback_dict.keys()
    models = StarCreativeFeedbackInfoDAL.query(equal_filters={'order_id__in': _order_ids})
    update_order_ids = {model.order_id: model for model in models}
    new_order_ids = list(set(_order_ids) - set(update_order_ids.keys()))
    for order_ids in split_list(_order_ids, 50):
        for order_id in order_ids:
            feedback = feedback_dict.get(order_id, None)
            if not feedback:
                continue
            if order_id in new_order_ids:
                StarCreativeFeedbackInfoDAL.new(**{
                    'spu_id': feedback.spu_id,
                    'order_id': feedback.order_id,
                    'star_id': feedback.star_id,
                    'user_role': feedback.user_role,
                    'feedback_level': feedback.feedback_level,
                    'feedback_info': feedback.feedback_info,
                    'feedback_time': feedback.feedback_time
                })
            elif order_id in update_order_ids.keys():
                record = update_order_ids[order_id]
                record.update(**{
                    'spu_id': feedback.spu_id,
                    'order_id': feedback.order_id,
                    'star_id': feedback.star_id,
                    'user_role': feedback.user_role,
                    'feedback_level': feedback.feedback_level,
                    'feedback_info': feedback.feedback_info,
                    'feedback_time': feedback.feedback_time
                })


if __name__ == '__main__':
    process()