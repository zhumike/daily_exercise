# coding=utf-8
"""
历史全量订单自动取消监控脚本
"""
import datetime
import sys

sys.path.insert(0, '/opt/tiger/ss_ad/ad_site_env/lib/python2.7/site-packages')
sys.path.append('/opt/tiger/toutiao/app/ad')

from star_common.const.const import AuthorTaskType
from star_common.const.order import OrderStatus, OrderAuditStatus
from star_common.utils.lark import send_msg_to_robot
from star_core.data.tqs_client import query_with_tqs_and_fetch_result
from star_common.dals.order import StarOrderDAL
import frame.logger as logging
from star_common.gateway.base_rpc import orders_client
from star_orders.service.order.order_status_flow_service import OrderStatusFlowService
from star_orders.business.order.order_auto_operation import get_no_auto_cancel_type

WARING_WEB_HOOK_URL = "https://open.feishu.cn/open-apis/bot/hook/511300073a704131ab576a78aa276237"


def recheck_order_cancel(order_id):
    date = datetime.date.today() - datetime.timedelta(days=8)
    date_str = datetime.date.strftime(date, "%Y%m%d")
    now_str = datetime.date.strftime(datetime.date.today() - datetime.timedelta(days=1), "%Y%m%d")
    video_type_no_auto_cancel = tuple(get_no_auto_cancel_type())
    need_cancel_order_status = (OrderStatus.receiving.value, OrderStatus.pre_checking.value)

    HIVE_SQL = """
                select
                    id
                from
                    ad_star.star_orders_dict
                where 
                    date = {}
                    and video_type NOT IN {}
                    and status IN {}
                    and from_unixtime(create_time, 'yyyyMMdd') <= {}
                """.format(now_str, video_type_no_auto_cancel,
                           need_cancel_order_status, date_str)
    rows = query_with_tqs_and_fetch_result(HIVE_SQL)[1:]
    order_ids = []
    success_ids = []
    fail_ids = []
    for row in rows[1:]:
        order_ids.append(int(row[0]))
    order_ids = [order_id]  # 测试任务id
    for order_id in order_ids:
        order = StarOrderDAL.query_by_id(order_id)
        if datetime.datetime.now() - datetime.timedelta(days=order.accept_expiration_day) < order.accept_available_time:
            continue
        if order.status != OrderStatus.receiving.value:
            continue
        try:
            orders_client.InnerOrderAutoCancelProcessor(order_id=order_id)
            logging.info("取消订单, order_id: %s", order_id)
        except Exception as err:
            fail_ids.append(order_id)
            logging.error("取消失败, order_id: %s, error: %s", order_id, err)
            continue
        success_ids.append(order_id)
    # 发单超过7天组件审核仍为失败的，自动取消
    for order_id in order_ids:
        order = StarOrderDAL.query_by_id(order_id)
        # if datetime.datetime.now() - datetime.timedelta(days=7) < order.create_time:
        #     continue
        if order.status != OrderStatus.pre_checking.value or order.audit_status == OrderAuditStatus.component_reject.value:
            continue
        try:
            orders_client.InnerOrderAutoCancelProcessor(order_id=order_id)
            logging.info("取消订单, order_id: %s", order_id)
        except Exception as err:
            fail_ids.append(order_id)
            logging.error("取消失败, order_id: %s, error: %s", order_id, err)
            continue
        success_ids.append(order_id)
    logging.info(
        "历史订单取消成功: %s, 取消失败: %s, 成功id: %s, 失败id: %s" % (len(success_ids), len(fail_ids), success_ids, fail_ids))
    send_msg_to_robot("历史全量订单自动取消监控",
                      "订单取消成功: %s, 取消失败: %s, 失败id: %s" % (len(success_ids), len(fail_ids), fail_ids),
                      at="yangqirui", webhook=WARING_WEB_HOOK_URL)


if __name__ == '__main__':
    test_id = sys.argv[1]
    try:
        recheck_order_cancel(order_id=test_id)
    except Exception as e:
        logging.error('[recheck_order_cancel] CronJob Failed, Error: %s', e)
        send_msg_to_robot("ALERT: 历史全量订单自动取消监控", '[recheck_order_cancel] CronJob Failed, Error: %s' % e, at="yangqirui",
                          webhook=WARING_WEB_HOOK_URL)