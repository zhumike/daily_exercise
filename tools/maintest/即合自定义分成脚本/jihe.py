# coding: utf-8
import sys
from decimal import Decimal

sys.path.insert(0, "/opt/tiger/ss_ad/ad_site_env/lib/python2.7/site-packages")
sys.path.insert(0, "/opt/tiger/toutiao/lib")
sys.path.insert(0, "/opt/tiger/toutiao/app/ad")
sys.path.insert(0, "/opt/tiger/toutiao/app/ad/star_orders")

from frame import logger as logging
from star_common.dals.order import StarOrderDAL
from star_common.const.order import OrderStatus, VideoAdSupplierOrderStatus
from star_common.const.const import OrderSnapshotBillType, AuthorTaskType
from star_orders.business.free_market.product_snapshot import FreeMarketProductSnapshotBusiness
from star_thrift_gen.idl.consts.market_thrift import SettlementType
from star_orders.business.order.order_business import OrderBusiness


def process(order_id, bonus_amount):
    order = StarOrderDAL.query({
        'id': order_id,
        'status': [
            VideoAdSupplierOrderStatus.video_ad_publish.value,
            OrderStatus.finished.value
        ]
    })

    if not order:
        print 'order not found!'
        return

    order = order[0]

    if (order.video_type == AuthorTaskType.free_market_task.value
            and not order.data_dict.get('free_market_sharing_limit')) or \
            order.video_type not in {AuthorTaskType.market_material.value, AuthorTaskType.free_market_task.value}:
        print 'order not applicable!'
        return

    freeze_amount = order.data_dict.current_freeze_amount

    if order.video_type == AuthorTaskType.market_material.value:
        base_amount = int(order.data_dict.order_template_info.template_base_price)
    else:
        spu_snapshot_info = FreeMarketProductSnapshotBusiness.get_snapshot_by_order_id(
            order.id, order.release_user_id
        ).get('spu_detail')
        settlement_info = None
        for settlement in spu_snapshot_info.settlements:
            if settlement.settlement_type == SettlementType.bonus:
                settlement_info = settlement
                break
        base_amount = Decimal(str(settlement_info.price)) / 1000
    author_income = int(base_amount + bonus_amount)
    to_update_dict = order.data_dict
    to_update_dict['actual_author_income'] = author_income
    order.update(data=to_update_dict)

    coupon_discount_snapshot = order.data_dict.get('platform_coupon_discount_snapshot')
    logging.info('coupon discount snapshot: %s' % coupon_discount_snapshot)
    if author_income > freeze_amount and not coupon_discount_snapshot:
        logging.error('order %s deduct amount error' % order.id)
        return
    if not order.data_dict.get('free_market_sharing_limit'):
        logging.error('order sharing limit missing! order_id: %s' % order.id)
        return

    author_income_rate = float(author_income) / float(
        base_amount + order.data_dict.get('free_market_sharing_limit') / 100)
    logging.info('author_income: %s, rate: %s' % (author_income, author_income_rate))

    author_subsidy = 0
    if coupon_discount_snapshot:
        author_subsidy = -int(author_income_rate * order.data_dict.get('platform_coupon_discount_snapshot'))
        unfreeze_amount = freeze_amount - author_income - author_subsidy
    else:
        unfreeze_amount = freeze_amount - author_income

    logging.info('author_subsidy: %s, unfreeze_amount: %s' % (author_subsidy, unfreeze_amount))
    OrderBusiness.approve_current_order(order, 0, unfreeze_amount=float(unfreeze_amount))


if __name__ == '__main__':
    _order_id, _bonus = int(sys.argv[1]), int(sys.argv[2])
    process(_order_id, _bonus)