# coding=utf-8
"""
即合订单 系统派单
定时任务 https://cloud.bytedance.net/cronjob/69132/job
"""
import sys
import os

sys.path.append('/opt/tiger/toutiao/app/ad')
sys.path.append('/home/zhoufengshun/repos/toutiao/app/ad/star_rpc/')
sys.path.append('/opt/tiger/ad/data')

from star_common.dals.creative_order import StarCreativeAssignOrderDAL
from star_common.dals.order import StarOrderDAL
from star_common.dals.material import StarMaterialOrderAssignDAL
from star_common.dals.market import StarMarketSpuDAL, StarMarketSpuWhitelistDAL

from star_common.const.order import VideoAdSupplierOrderStatus
from star_common.const.material import MaterialTemplateMatchMode, CreativeOrderAssignRange
from star_common.const.market.market import SpuSource, OrderMode, SpuStatus, SpuLimit, TargetType

from star_common.gateway.euler_base_rpc import orders_client

from frame import logger as logging
import datetime


def config():
    from star_common.storage.db_session import set_all_data_read_only
    set_all_data_read_only()


# 派单全员可见
def assign_all_author(order, spu_id):
    # 星图的希望
    if order.release_user_id == 1639752636991496:
        return []

    assign_records = StarMaterialOrderAssignDAL.query({
        'order_id': order.id
    })
    # 已经分派的达人id
    dispatched_author_ids = [_.author_id for _ in assign_records]

    whitelists = StarMarketSpuWhitelistDAL.query({
        'spu_id': spu_id,
        'target_type': TargetType.author.value
    })
    # spu白名单内的达人id
    spu_whitelist_author_ids = set([whitelist.target_id for whitelist in whitelists])
    # 需要新增的达人id
    need_add_author_id = list(set(spu_whitelist_author_ids) - set(dispatched_author_ids))

    for author_id in need_add_author_id:
        StarMaterialOrderAssignDAL.new(**{
            'order_id': order.id,
            'match_mode': MaterialTemplateMatchMode.system_assign.value,
            'author_id': author_id,
            'status': 1
        })

    return need_add_author_id


def get_assigns():
    # 这部分时间配置后续走tcc吧
    # 可以跟orders服务里面的tcc保持一致
    start_time = datetime.datetime.now() - datetime.timedelta(days=7)
    last_assign_time = datetime.datetime.now() - datetime.timedelta(days=1)
    assigns = StarCreativeAssignOrderDAL.query({
        'need_assign': 1,
        # 'create_time__gt': start_time,
        'last_assign_time__lt': last_assign_time
    })
    return assigns


def main():
    assigns = get_assigns()

    orders = StarOrderDAL.query_by_ids([_.id for _ in assigns])
    order_id_2_order = {order.id: order for order in orders}

    # 派单
    for assign in assigns:
        order = order_id_2_order.get(assign.id)
        if not order:
            logging.warning("未找到对应的order  assign_id = {}".format(assign.id))
            continue

        spu_id = order.data.get('spu_id', 0)
        spu = StarMarketSpuDAL.query_by_id(spu_id)
        if not spu or spu.order_mode != OrderMode.dispatch.value:
            logging.warning("未找到对应的spu 或 spu不是系统指派 order_id = {}".format(order.id))
            continue

        # 已接单情况  更新assign状态
        if order.status not in [VideoAdSupplierOrderStatus.receiving.value]:
            assign.update(need_assign=0)
            logging.info("订单状态已变更  无需再派单  order_id = {}".format(order.id))
            continue

        if order.create_time + datetime.timedelta(days=2) < datetime.datetime.now():
            # 超过2天 改为全员可见
            added_author_id = assign_all_author(order, spu_id)
            assign.update(need_assign=0)
            logging.info("订单转为全员可见 order_id = {}  新增的达人id = {}".format(order.id, added_author_id))
        else:
            # 正常派单
            try:
                author_ids = orders_client.InnerCreativeOrderAssign(order_id=order.id, assign_num=3).author_ids
                logging.info("订单派单成功 order_id = {}  author_ids = {}".format(order.id, author_ids))
            except Exception as err:
                logging.info("订单派单失败 order_id = {}  err = {}".format(order.id, err))


if __name__ == '__main__':
    # config()
    main()