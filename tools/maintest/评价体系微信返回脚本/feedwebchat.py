# coding=utf-8


try:
    from typing import Dict
except ImportError:
    pass

import datetime
import sys
sys.path.insert(0, '/opt/tiger/ss_ad/ad_site_env/lib/python2.7/site-packages')
sys.path.insert(0, '/opt/tiger/toutiao/lib')
sys.path.insert(0, '/opt/tiger/toutiao/app/ad')
sys.path.insert(0, '/opt/tiger/toutiao/app/ad/star_author')
import os
os.environ['SERVICE_MESH_EGRESS_ADDR'] = '/opt/tiger/toutiao/var/service/%s.mesh/rpc.egress.sock' % os.getenv('TCE_PSM')

from star_core.config.base import IS_DEV, IS_BOE
from star_core.data.tqs_client import query_with_tqs_and_fetch_result
from star_common.gateway.euler_base_rpc import generic_client
from star_common.utils.util import split_list
from star_common.utils.converter import datetime2string
from star_thrift_gen.idl.generic_thrift import MessageChannelType


class MessageInfo(object):
    def __init__(self, author_id, nick_name, demander_count, order_count):
        self.author_id = author_id
        self.nick_name = nick_name
        self.demander_count = demander_count
        self.order_count = order_count


def query_stat_from_hive():
    # type: () -> Dict
    """
    获取创意定制反馈信息
    """
    if IS_DEV or IS_BOE:
        return {}
    date_str = datetime2string(datetime.datetime.now() - datetime.timedelta(days=1), format='%Y%m%d')
    hive_sql = '''
        SELECT
            t3.id as author_id,  
            t3.nick_name,
            count(DISTINCT(t1.star_id)) AS demander_count,
            count(DISTINCT(t1.order_id)) AS order_count
        FROM    
            ad_star.star_creative_feedback_info t1,
            ad_site.star_orders_dict t2,
            ad_star.star_author_info_creator_dict t3
        WHERE   t1.date = '%s'
        AND     t2.date = '%s'
        AND     t3.date = '%s'
        AND     t1.order_id = t2.id
        AND     t2.producer_id = t3.id
        GROUP BY
            t3.id,
            t3.nick_name
        HAVING  demander_count > 0
        AND     order_count > 0
    ''' % (date_str, date_str, date_str)
    rows = query_with_tqs_and_fetch_result(hive_sql)
    if not rows or len(rows) <= 1:
        print 'empty rows: ', rows
        return {}

    return {_[0]: MessageInfo(*_) for _ in rows[1:]}


def process():
    message_dict = query_stat_from_hive()
    _author_ids = message_dict.keys()
    for author_ids in split_list(_author_ids, 50):
        for author_id in author_ids:
            phone_content_param = {
                'nick_name': message_dict[author_id].nick_name,
                'demander_count': str(message_dict[author_id].demander_count),
                'order_count': str(message_dict[author_id].order_count),
                'feedback_count': str(message_dict[author_id].order_count),
            }
            wechat_content_param = {
                'first': "您好 {}，{}!".format(message_dict[author_id].nick_name, "收到新的客户评价"),
                'keyword1': "",
                'keyword2': "收到新的客户评价!昨日共收到来自{}个客户关于{}个订单的{}条评价。".
                    format(message_dict[author_id].demander_count,
                           message_dict[author_id].order_count,
                           message_dict[author_id].order_count),
                'keyword3': datetime2string(datetime.datetime.now()),
                'remark': "请登录即合桌面端在「订单管理」或「即合服务管理」中查看。",
            }
            generic_client.InnerSendMessage(
                message_type_list=[MessageChannelType.phone],
                phone_template_id=17328,
                content_param=phone_content_param,
                star_ids=[6641178755068854276L],
            )
            generic_client.InnerSendMessage(
                message_type_list=[MessageChannelType.creative_wechat_app],
                wechat_template_id="WnxkFzAWj7YDc3a6c8KFWz3GFTR78CChiARePktsp_I",
                content_param=wechat_content_param,
                star_ids=[6641178755068854276L],
            )


if __name__ == "__main__":
    process()