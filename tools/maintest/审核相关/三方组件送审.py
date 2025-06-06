# coding=utf-8

import sys

sys.path.insert(0, '/opt/tiger/ss_ad/ad_site_env/lib/python2.7/site-packages')
sys.path.append('/opt/tiger/')
sys.path.append('/opt/tiger/toutiao/app/ad')
sys.path.insert(0, '/opt/tiger/toutiao/webarch_lib')

from frame import logger as logging, get_current_logid

from star_common.mq.bmq_producer import get_bmq_producer
from star_core.common.exception import SolarException
from star_common.const.code import SupplierStatusCode
from star_thrift_gen.thrift_gen.orders.ttypes import LinkComponent, LinkStatus, LinkType
from star_common.conf.init_conf import IS_DEV, IS_BOE
from pykafkaclient.kafka_proxy2.kafka_proxy import KafkaProxy
from star_common.dals.component import StarLinkComponentDAL, StarIndustryAnchorDAL
from star_core.http_api.lark import send_msg_to_robot

component_producer = None


def get_producer():
    global component_producer
    if not component_producer:
        if IS_DEV or IS_BOE:
            component_producer = get_bmq_producer(cluster_name='bmq_boe_test', topic='ad_unaudit_in_star_link')
        else:
            component_producer = get_bmq_producer(cluster_name='bmq_adsys', topic='ad_unaudit_in_star_link')
    return component_producer


def send_audit_industry_anchor(anchor_id):
    anchor = StarIndustryAnchorDAL.query_by_id(anchor_id)
    if not anchor:
        raise SolarException(SupplierStatusCode.ERROR_VALIDATION, u'anchor_id=%s不存在' % anchor_id)
    if anchor.industry_anchor_status == LinkStatus.Valid:
        raise SolarException(SupplierStatusCode.ERROR_VALIDATION, u'anchor_id=%s已审核通过无需送审' % anchor_id)

    task = new_send_task(product_name='star_industry_anchor')
    task.set_log_id(str(get_current_logid()))
    task.set_obj_id(int(anchor_id))
    task.set_object_name(anchor.industry_anchor_name.encode('utf-8'))
    mq_body = task.get_mq_body()

    logging.info('send_audit_by_task anchor = %s', task)

    producer = get_producer()
    producer.write_msgs(mq_body, block=True)
    status = LinkStatus.Auditing
    anchor.update(industry_anchor_status=LinkStatus.Auditing, audit_reject_reason='')
    return status


def new_send_task(product_name='star_link'):
    try:
        from pylib.audit_task.audit_task import AuditTask
        from pylib.const.audit_const import MsgTypeConst
        from pylib.const.audit_const import ObjectTypeConst

        task = AuditTask()
        task.set_object_type(ObjectTypeConst.OBJECT_TYPE_MATERIALS)
        task.set_msg_type(MsgTypeConst.MSG_TYPE_SEND)
        task.set_product(product_name)

        return task
    except:
        logging.error('import audit_lib error. not ok if tce start')
        send_msg_to_robot('audit_lib包引入失败', 'new send task error', at='yekai.klaus')
        raise SolarException(SupplierStatusCode.ERROR_SYSTEM_UNKNOWN, u'系统内部错误，请联系管理员')


if __name__ == '__main__':
    test_id = sys.argv[1]
    send_audit_industry_anchor(anchor_id=test_id)