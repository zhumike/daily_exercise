# -*- coding: utf-8 -*-
'''
@Author : zhuzhenzhong
@File : tr.py
'''
tests/author/test_LogoffAuthor.py

@pytest.mark.usefixtures('setup_class')
@pytest.mark.usefixtures('rpc_env')
class TestLogoffAuthor:
    @pytest.fixture(autouse=True)
    def _setup(self, author_client):
        self._client = author_client

    @allure.title('正常注销达人')
    def test_success(self):
        req = {
            's_star_id': Logoff_Test_Author,
        }

        if os.environ['RPC_ENV']  in ['boe_star_auto_test','boe_star_pre_release','boe_star_coverage_test']:
            rsp = rpc.request(self._client, 'LogoffAuthor', req)
            assert rsp['BaseResp']['StatusCode'] == 0
            query_sql = "SELECT *  FROM `ad_supplier`.`star_author_info_under_fans_limit` WHERE `id` = %d" % (Logoff_Test_Author)
            expect = session.execute(query_sql)
            assert_that(expect[0]['status']).is_equal_to(4)
            assert_that(expect[0]['core_user_id']).is_equal_to(0)
            assert_that(expect[0]['short_id']).is_equal_to(0)
            assert_that(expect[0]['unique_id']).is_equal_to('')
            assert_that(expect[0]['withdraw_phone']).is_equal_to('')
            print(os.environ['RPC_ENV'])
        else:
            logger.info("skip")