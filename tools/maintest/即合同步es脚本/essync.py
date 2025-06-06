# -*- coding: utf-8 -*-
# @Time : 2021/12/2 4:03 下午
# @Author : zhuzhenzhong

import sys

from star_orders.business.search.order_search.task_order_sync_to_es.material_task_sync_es_business import MaterialTaskSyncEsBusiness
from star_orders.business.search.demand_search.task_demand_sync_to_es.task_material_demand_sync_es_business import \
        TaskMaterialDemandSyncEsBusiness
from star_common.dals.order import StarOrderDAL


def test25(test_id):
    order_id = test_id
    order = StarOrderDAL.query_by_id(order_id)
    TaskMaterialDemandSyncEsBusiness.write_to_es(order.demand_id)
    MaterialTaskSyncEsBusiness.write_to_es(order_id)
    print "finish"

if __name__ == '__main__':
    test_id=int(sys.argv[1])
    test25(test_id)
