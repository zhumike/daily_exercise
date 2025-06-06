# -*- coding: utf-8 -*-
'''
@Author : zhuzhenzhong
@File : settlement.py
'''
# -*- coding: utf-8 -*-
'''
@Author : zhuzhenzhong
@File : test_TransferMoney.py
'''

import logging
import os
import allure
import pytest
from lib import rpc
from lib.db import session
from .constants import author_real_id
from assertpy import assert_that
import random
import  time

cur_dir = os.path.dirname(os.path.abspath(__file__))
logger = logging.getLogger(__name__)

"""
https://cloud.bytedance.net/bam/rd/ad.star.settlement/api_doc/show_doc?cluster=default&version=1.0.1301&api_branch=feat_add_settlement_biz_type&endpoint_id=498493
"""
class TestTransferMoney:
    @pytest.fixture(autouse=True)
    def _setup(self, settlement_client):
        self._client = settlement_client



    @pytest.fixture(scope='function')
    def teardown_function(self):

        #初始化数据
        global biz_order_id
        global request_id
        biz_order_id = random.randint(0, 10000000000)
        request_id = str(random.randint(0, 10000000)+random.randint(0, 1000))

        yield  #数据清理恢复，每次测试完毕后清除数据记录
        clear_sql = "DELETE   from  `ad_supplier`.`star_user_trade_record`  WHERE `order_id` = %d   LIMIT 1" % (biz_order_id)
        session.execute(clear_sql)  # 清除封禁落表测试数据

    @pytest.mark.usefixtures('teardown_function')
    @allure.title("打款测试-野生达人")
    def test_success(self):
        req = {
            "app_id": 1581,
            "order_triple": {
                "biz_type": 4,
                "biz_id": 19,
                "biz_order_id": biz_order_id
            },
            "request_id": request_id,
            "amount": 1000,
            "payee": {
                "participant_type": 3,
                "star_wallet": {
                    "star_id": author_real_id
                }
            },
            "extra": {
                "task_type": "1",
                "deduct_amount": "1000",#单位：分
                "user_price": "1000",
                "order_amount": "1000",
                "order_channel": "star",
                "biz_order_name": "打款野生达人",
                "origin_order_id": str(biz_order_id),
                "star_ad_union_order": "1"
            }
                }
        rsp = rpc.request(self._client, 'TransferMoney', req)
        assert rsp['BaseResp']['StatusCode'] == 0
        time.sleep(1)
        sql1 = "SELECT *  from  star_user_trade_record  where order_id = '%d' " % (biz_order_id)
        expect = session.execute(sql1)
        assert_that(expect[0]['user_id']).is_equal_to(author_real_id)

