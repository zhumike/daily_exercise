# -*- coding: utf-8 -*-
# @Time : 2022/3/29 2:37 下午
# @Author : zhuzhenzhong
#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import sys

sys.path.insert(0, '/opt/tiger/ss_ad/ad_site_env/lib/python2.7/site-packages')
sys.path.insert(0, '/opt/tiger/')
sys.path.insert(0, '/opt/tiger/toutiao/app/ad')
sys.path.insert(0, '/opt/tiger/toutiao/webarch_lib')
sys.path.insert(0, '/opt/tiger/toutiao/app/ad/star_orders')
from star_orders.business.audit.ad_audit_v2 import StarPreAuditBusinessV2
from star_common.dals.order import StarOrderDAL
from star_common.storage.tcc import StarConfig
from star_common.dals.demand import StarDemandDAL

if __name__ == "__main__":
    order_id_input, item_id_input=int(sys.argv[1]), int(sys.argv[2])
    order = StarOrderDAL.query_by_id(order_id_input)
    demand = StarDemandDAL.query_by_id(order.demand_id)
    item_id = item_id_input
    audit_config = StarConfig.get('star_item_pre_audit_control')
    StarPreAuditBusinessV2.process(order, item_id, demand, audit_config)