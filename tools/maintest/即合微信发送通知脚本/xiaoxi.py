# coding=utf-8

import sys
import os

os.environ['SERVICE_MESH_EGRESS_ADDR'] = '/opt/tiger/toutiao/var/service/%s.mesh/rpc.egress.sock' % os.getenv('TCE_PSM')

sys.path.insert(0, '/opt/tiger/toutiao/app/ad/star')
sys.path.append('/opt/tiger/toutiao/app/ad')
sys.path.append('/home/zhoufengshun/repos/toutiao/app/ad/star_rpc/')
sys.path.append('/opt/tiger/ad/data')

try:
    import google.protobuf
    from bytedeventbus.producer.producer import EventbusProducer
    from bytedeventbus.producer.event_builder import EventBuilder
except:
    pass


def config():
    from star_common.storage.db_session import set_all_data_read_only
    set_all_data_read_only()


def test20():
    from star_common.gateway.base_rpc import orders_client
    from star_orders.const.order.order_notification import CreativeOrderFlowEvent

    order_id = 7025563325744332844
    orders_client.InnerCreativeOrderNotify(order_id=order_id, event_type=CreativeOrderFlowEvent.prepay_order_accepted)
    print "finish"

if __name__ == '__main__':
    # config()
    test20()