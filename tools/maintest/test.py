# -*- coding: utf-8 -*-
'''
@Author : zhuzhenzhong
@File : test.py
'''
"""
@Author : zhuzhenzhong
"""
from assertpy import assert_that
from lib.db import session
import logging
import pytest
import allure
from lib import rpc
from .constants import demander_id
logger = logging.getLogger(__name__)

class TestDemanderGetUniversalDemandList:

    """
https://cloud.bytedance.net/bam/rd/ad.star.goplatform/api_doc/show_doc?version=1.0.399&cluster=default&endpoint_id=225276
    """

    @pytest.fixture(autouse=True)
    def _setup(self, goplatform_client):
        self._client = goplatform_client

    @allure.title("客户查询demand列表")
    def test_success(self):
        req = {
            "demander_id": demander_id,
            "app_id": 1581,#星图应用
            "query": {
                "time_range_query": {
                    "start_time": 1683704916,
                    "end_time": 1691653716
                }
            },
            "page": 1,
            "limit": 2,
            "order_limit": 2,
        }
        rsp = rpc.request(self._client, 'DemanderGetUniversalDemandList', req)
        assert rsp['BaseResp']['StatusCode'] == 0
        for i in range(len(rsp['demand_info_list'])):
            #demand_info信息校验
            sql_query = "select * from star_demand where id = %d" % (rsp['demand_info_list'][i]['demand_info']['demand_id'])
            expect = session.execute(sql_query)
            assert_that(expect[0]['name']).is_equal_to(rsp['demand_info_list'][i]['demand_info']['demand_name'])
            assert_that(expect[0]['platform_source']).is_equal_to(rsp['demand_info_list'][i]['demand_info']['platform_source'])
            assert_that(expect[0]['task_category']).is_equal_to(rsp['demand_info_list'][i]['demand_info']['task_category'])
            assert_that(expect[0]['group_id']).is_equal_to(rsp['demand_info_list'][i]['demand_info']['group_id'])
            #校验冻结资金
            sql_query = "select * from star_bill_info where order_id = %d and op_type = '1' " % (rsp['demand_info_list'][i]['demand_info']['demand_id'])
            expect = session.execute(sql_query)
            sum = 0
            for j in range(len(expect)):
                sum  = sum + expect[j]['amount']
            assert_that(int(sum/1000)).is_equal_to(rsp['demand_info_list'][i]['total_pay'])
            #校验订单
            sql_query2 = "select * from star_orders where id = %d " % (rsp['demand_info_list'][i]['order_info_list'][0]['order_info']['id'])
            expect2 = session.execute(sql_query2)
            assert_that(expect2[0]['status']).is_equal_to(rsp['demand_info_list'][i]['order_info_list'][0]['order_info']['status'])
            assert_that(expect2[0]['video_type']).is_equal_to(rsp['demand_info_list'][i]['order_info_list'][0]['order_info']['video_type'])
            assert_that(expect2[0]['order_type']).is_equal_to(rsp['demand_info_list'][i]['order_info_list'][0]['order_info']['order_type'])
            #校验客户信息
            sql_query3 = "select * from star_demander_information where id = %d " % (rsp['demand_info_list'][i]['demander_info']['id'])
            expect3 = session.execute(sql_query3)
            assert_that(expect3[0]['name']).is_equal_to(rsp['demand_info_list'][i]['demander_info']['name'])

    @allure.title("客户查询demand列表,覆盖部分可选查询参数")
    def test_success2(self):
        req = {
            "demander_id": demander_id,
            "app_id": 1581,#星图应用
            "query": {
                "marketing_type":1,
                "task_category":1,
                "producer_type":1,
                "universal_settlement_type":2,
                "component_type":1,
                "universal_order_status":3,
                ""
                "time_range_query": {
                    "start_time": 1683704916,
                    "end_time": 1691653716
                },
                "platform_source":1,
                "video_type":1,
                "query_status":0
            },
            "page": 1,
            "limit": 2,
            "order_limit": 2,
        }
        rsp = rpc.request(self._client, 'DemanderGetUniversalDemandList', req)
        assert rsp['BaseResp']['StatusCode'] == 0
        for i in range(len(rsp['demand_info_list'])):
            #demand_info信息校验
            sql_query = "select * from star_demand where id = %d" % (rsp['demand_info_list'][i]['demand_info']['demand_id'])
            expect = session.execute(sql_query)
            assert_that(expect[0]['name']).is_equal_to(rsp['demand_info_list'][i]['demand_info']['demand_name'])
            assert_that(rsp['demand_info_list'][i]['demand_info']['platform_source']).is_equal_to(1)
            assert_that(rsp['demand_info_list'][i]['demand_info']['task_category']).is_equal_to(1)
            assert_that(expect[0]['group_id']).is_equal_to(rsp['demand_info_list'][i]['demand_info']['group_id'])
            #校验冻结资金
            sql_query = "select * from star_bill_info where order_id = %d and op_type = '1' " % (rsp['demand_info_list'][i]['demand_info']['demand_id'])
            expect = session.execute(sql_query)
            sum = 0
            for i in range(len(expect)):
                sum  = sum + expect[i]['amount']
            assert_that(int(sum/1000)).is_equal_to(rsp['demand_info_list'][i]['total_pay'])
            #校验订单
            sql_query2 = "select * from star_orders where id = %d " % (rsp['demand_info_list'][i]['order_info_list'][0]['order_info']['id'])
            expect2 = session.execute(sql_query2)
            assert_that(expect2[0]['status']).is_equal_to(rsp['demand_info_list'][i]['order_info_list'][0]['order_info']['status'])
            assert_that(expect2[0]['video_type']).is_equal_to(rsp['demand_info_list'][i]['order_info_list'][0]['order_info']['video_type'])
            assert_that(expect2[0]['order_type']).is_equal_to(rsp['demand_info_list'][i]['order_info_list'][0]['order_info']['order_type'])
            #校验客户信息
            sql_query3 = "select * from star_demander_information where id = %d " % (rsp['demand_info_list'][i]['demander_info']['id'])
            expect3 = session.execute(sql_query3)
            assert_that(expect3[0]['name']).is_equal_to(rsp['demand_info_list'][i]['demander_info']['name'])


    @allure.title("覆盖客户达人昵称筛选参数")
    def test_success3(self):
        req = {
            "demander_id": demander_id,
            "app_id": 1581,#星图应用
            "query": {
                "time_range_query": {
                    "start_time": 1683704916,
                    "end_time": 1691653716
                },
                "demander_name":"用户",
                "author_nick_name":"用户",
                "search_key":"任务"
            },
            "page": 1,
            "limit": 2,
            "order_limit": 2,
        }
        rsp = rpc.request(self._client, 'DemanderGetUniversalDemandList', req)
        assert rsp['BaseResp']['StatusCode'] == 0
        for i in range(len(rsp['demand_info_list'])):
            assert_that(rsp['demand_info_list'][i]['demand_info']['demand_name']).contains("任务")
            assert_that(rsp['demand_info_list'][i]['demander_info']['name']).contains("用户")
            assert_that(rsp['demand_info_list'][i]['order_info_list'][0]['author_info']['nick_name']).contains("用户")

    @allure.title("缺少入参，报错")
    def test_fail(self):
        req = {
            "demander_id": demander_id,
            "app_id": 1581,#星图应用
            "page": 1,
            "limit": 2,
            "order_limit": 2,
        }
        rsp = rpc.request(self._client, 'DemanderGetUniversalDemandList', req)
        assert rsp['BaseResp']['StatusCode'] == 120002

