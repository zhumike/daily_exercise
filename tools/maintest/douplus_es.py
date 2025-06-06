# -*- coding: utf-8 -*-
# @Time : 2021/9/17 4:48 下午
# @Author : zhuzhenzhong


#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import sys

sys.path.insert(0, '/opt/tiger/ss_ad/ad_site_env/lib/python2.7/site-packages')
sys.path.insert(0, '/opt/tiger/')
sys.path.insert(0, '/opt/tiger/toutiao/app/ad')
sys.path.insert(0, '/opt/tiger/toutiao/webarch_lib')
sys.path.insert(0, '/opt/tiger/toutiao/app/ad/star_orders')

try:
    from bytedeventbus.producer.producer import EventbusProducer
    from bytedeventbus.producer.event_builder import EventBuilder
except:
    pass
from star_orders.service.search.search_service import SearchService
from star_common.dals.demand import StarDemandDAL
from star_common.dals.campaign import StarCampaignDAL


def Test_inner_sync_campaign_to_es(campaign_id):
    campaign = StarCampaignDAL.query_by_id(campaign_id)
    if not campaign:
        return
    demands = StarDemandDAL.query(equal_filters={'campaign_id': campaign_id})
    for demand in demands:
        print demand.id
        SearchService.inner_sync_demand_to_es(demand_id=demand.id, task_category=demand.task_category)
    return

if __name__ == "__main__":
    campaign = StarCampaignDAL.query_by_id(7008816307353174060)
    Test_inner_sync_campaign_to_es(campaign.id)