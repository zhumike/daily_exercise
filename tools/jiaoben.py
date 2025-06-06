# -*- coding: utf-8 -*-
'''
@Author : zhuzhenzhong
@File : jiaoben.py
'''
"""
@author: zhuzhenzhong
@contact: zhuzhenzhong@bytedance.com
"""

import pytest
import allure
from lib import rpc
from assertpy import assert_that
from lib.db import star_user_session as session
from .constants import demander_id

"""
https://cloud.bytedance.net/bam/rd/ad.star.godemander/api_doc/show_doc?version=1.0.450&api_branch=feat_rank_subscribe&endpoint_id=929590
"""


#初始化数据准备
record_query_sql = "SELECT * FROM `ad_star_user`.`star_base_project_author_list` where `platform_source`='1' and `platform_channel`='1' order by `create_time` desc LIMIT 0,100"
receiver_list = session.execute(record_query_sql)
global project_id
project_id = receiver_list[0]['project_id']
author_list_id = receiver_list[0]['author_list_id']

record_query_sql = "SELECT * FROM `ad_star_user`.`star_author_list` where `id` = %d "%(author_list_id)
demander_own = session.execute(record_query_sql)
global demander_own_id
demander_own_id = demander_own[0]['owner_id']


class TestDemanderGetAuthorListInfo:
    @pytest.fixture(autouse=True)
    def _setup(self, go_demander_client):
        self._client = go_demander_client

    @allure.title("获取项目相似达人清单")
    def test_success(self):
        req = {
            "project_id": project_id,
            "s_demander_id": demander_own_id,
            "platform_channel": 1,
            "platform_source": 1,
            "page":1,
            "limit":10
        }
        res = rpc.request(self._client, 'DemanderGetAuthorListInfo', req)
        assert res['BaseResp']['StatusCode'] == 0
        assert_that(res).contains_key("author_lists")
        assert_that(res['project_author_list']).is_not_none()

    @allure.title("客户非项目owner")
    def test_fail(self):
        req = {
            "project_id": project_id,
            "s_demander_id": 1234511,
            "platform_channel": 1,
            "platform_source": 1,
            "page":1,
            "limit":10
        }
        res = rpc.request(self._client, 'DemanderGetAuthorListInfo', req)
        assert res['BaseResp']['StatusCode'] == 100000