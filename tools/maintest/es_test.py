#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import sys

sys.path.insert(0, '/opt/tiger/ss_ad/ad_site_env/lib/python2.7/site-packages')
sys.path.insert(0, '/opt/tiger/')
sys.path.insert(0, '/opt/tiger/toutiao/app/ad')
sys.path.insert(0, '/opt/tiger/toutiao/webarch_lib')
sys.path.insert(0, '/opt/tiger/toutiao/app/ad/star_orders')
from star_orders.service.search.search_service import SearchService
from star_common.dals.demand import StarDemandDAL
from star_common.dals.order import StarOrderDAL


def Test_inner_sync_campaign_to_es(demand_id):
    if demand_id == 0:
        print "请输入 Demand Id"
    demand = StarDemandDAL.query_by_id(demand_id)
    SearchService.inner_sync_campaign_to_es(campaign_id=demand.campaign_id)
    SearchService.inner_sync_demand_to_es(demand_id=demand.id, task_category=demand.task_category)
    orders = StarOrderDAL.query(equal_filters={'demand_id': demand_id})
    for _ in orders:
        SearchService.inner_sync_order_to_es(_.id, demand.task_category)
    return


if __name__ == "__main__":
    print "=" * 100
    print "=" * 100
    demand_id = sys.argv[1] if len(sys.argv) > 1 else 0
    print "同步demand_id: ", demand_id
    Test_inner_sync_campaign_to_es(demand_id)