#!/usr/bin/env python
# encoding: utf-8
"""
@author: taojin
@contact: taojin.20200520@bytedance.com
@file: mock_base.py
@time: 2021/1/14 10:32
"""

try:
    from bytedeventbus.producer.producer import EventbusProducer
    from bytedeventbus.producer.event_builder import EventBuilder
except:
    pass

import json
import random
import datetime
import sys
import time
import argparse
from collections import defaultdict

import requests
from frame import logger as logging

sys.path.insert(0, "/opt/tiger/toutiao/app/ad")

from star_common.const.author.author import TaskCategory
from star_orders.service.mission_platform.sync_mission_service import SyncMissionService
from star_orders.service.search.search_service import SearchService

from star_orders.dals.item_cost_daily import StarItemCostDailyDAL, StarChallengeItemValidVVDAL
from star_orders.const.challenge import CostType, ChallengeAuditStatus
from star_common.dals.mission_platform_dal import StarChallengeOrderDAL, StarUniversalChallengeDAL
from star_common.dals.challenge import ChallengeDAL, ChallengeItemStatDAL, ChallengeStatDAL, ConvertDetailDAL, \
    ChallengeRewardDAL, StarChallengeItemExtraInfoDAL
from star_common.gateway.base_rpc import challenge_client, orders_client, generic_client
from star_common.const.order.challenge import ChallengeStatus, ChallengePayType, ChallengeEvaluateType
from star_orders.business.challenge.challenge import ChooseChallengeItemCpmHandler, ChooseChallengeItemCpsHandler, \
    ChooseChallengeItemCpaHandler, ChooseChallengeItemWithoutRewardHandler, ChooseChallengeItemAdIncomeHandler, \
    ChooseChallengeItemSecretCpaHandler
from star_common.utils.easy_dict import EasyDict
from star_orders.business.challenge.challenge import AdminSendChallengeRewardHandler
from star_common.utils.converter import get_today_zero_clock
from star_common.const.component.component import ItemComponentType

from star_common.dals.mission_platform_dal import StarChallengeOrderDAL
from star_common.dals.author import StarAuthorInfoDAL, StarAuthorInfoUnderFansLimitDAL
from star_common.dals.demand import StarDemandDAL

author_id_item_ids = {
    6887856234532175879: [6916428281394810120, 6916428281394793736, 6916361535484939527],  # Larva 野生达人
    6885640802911911949: [6916426650108300557, 6916426650108398861, 6916426650108448013],  # 帅气的测试  MCN达人
    6909696218012581896: [6922687876912254215, 6922687778195098888, 6922687649358630158],  # MCN达人1， MCN达人，繁星计划达人
    6909696463530360846: [6922689285728537869, 6922689182645243150, 6922689079582805262],  # MCN达人2， MCN达人
    6901899849692626958: [6969760316859157804, 6969759917427363116, 6969380407343172908],  # 繁星计划达人，
    6978785489935401004: [6979185437940354348],
    6976151894242639916: [6976616293483007276],
}


def get_random(count, total=100, return_float=True):
    """功能为返回一个list，个数为count, 总和为total"""
    ceil = total / count - 1
    if ceil <= 0:
        return [1 for _ in range(count)]
    res = [random.randint(1, ceil) for _ in range(count - 1)]
    res.append(total - sum(res))
    if return_float:
        return [float(_) for _ in res]
    return res


class MockBase(object):
    def __init__(self, challenge_id, choose_handler, env='prod'):
        self.challenge_id = challenge_id
        self.choose_hander = choose_handler
        self.consume_percent = 80.0
        self.env = env
        self.challenge = ChallengeDAL.query_by_id(self.challenge_id)
        self.demand = StarDemandDAL.query_by_id(self.challenge_id)

        self.consume_budget = self.challenge.budget / 1000 * (float(self.consume_percent) / 100)
        self.budgets_for_users = [self.consume_budget * x / 100 for x in get_random(len(author_id_item_ids.keys()))]
        self.delta = self.challenge.expiration_time_end.date() - self.challenge.expiration_time.date()

    def main(self, action):
        action_list = [
            self.audit_pass,  # 1
            self.participate,  # 2
            self.bind_item,  # 4
            self.audit_item,  # 8
            self.gen_convert_stat,  # 16
            self.mock_choose_reward,  # 32
            self.mock_challenge_bulletin_status,  # 64
            self.mock_challenge_reward_and_bulletin,  # 128
            self.mock_challenge_wait_send_reward,  # 256
            self.mock_challenge_send_reward,  # 512
            self.clear_up  # 1024
#审核投稿任务
# 达人参与
# 达人上传视频
# 视频审核通过
# mock转化数据
# 进入选稿状态(仅按等级结算)
# 公示期
# 计费期
# 待发奖
# 发奖
        ]
        for i in range(len(action_list)):
            if action & (1 << i):
                action_list[i]()

    def sync_challenge(self):
        try:
            SearchService.inner_sync_demand_to_es(self.challenge.demand_id, TaskCategory.douyin_challenge.value)
            SyncMissionService.inner_sync_mission(self.challenge.demand_id, TaskCategory.douyin_challenge.value)
            for order in StarChallengeOrderDAL.query({'demand_id': self.challenge.demand_id}):
                SearchService.inner_sync_order_to_es(order.id, TaskCategory.douyin_challenge.value)
        except Exception as err:
            print err
            pass

    def audit_pass(self, user_id=6594597963010408461):
        challenge = StarUniversalChallengeDAL.query_universal_challenge(self.challenge_id, 1)
        if not challenge:
            self.sync_challenge()
        params = dict(
            dev_user_id=user_id,
            s_employee_id=user_id,
            s_user_id=user_id,
            service_name='orders.AdStarOrdersService',
            service_method='AdminChallengeAudit',
            ignore_sign=True,
            audit_status=1,
            ban_reason_detail='',
            challenge_id=self.challenge_id
        )
        response = requests.post('http://star-boe.bytedance.net/h/api/gateway/handler_post/', json=params)
        print response.json()

    def participate(self):
        logging.info('in process: participate.%s', '=' * 20)
        params = dict(
            challenge_id=str(self.challenge_id),
            service_name='challenge.AdStarChallengeService',
            service_method='ParticipateChallenge',
            dev_user_id=0,
            ignore_sign=True,
        )
        for author_id in author_id_item_ids.keys():
            params['dev_user_id'] = author_id
            logging.info('in process: participate.%s', params)
            response = requests.post('http://star-boe.toutiao.com/h/api/gateway/handler_post/', json=params,
                                     headers={'x-tt-env': self.env, 'x-use-boe': '1',
                                              'Host': 'star-boe.toutiao.com'})
            logging.info(response.json())

    def bind_item(self):
        for author_id, item_ids in author_id_item_ids.items():
            core_user_id = (StarAuthorInfoDAL.query_by_id(author_id) or StarAuthorInfoUnderFansLimitDAL.query_by_id(
                author_id)).core_user_id
            order = StarChallengeOrderDAL.query_one({'demand_id': self.challenge_id, 'producer_id': author_id})
            demand_or_order_id = order.id
            for item_id in item_ids:
                challenge_client.InnerBindAwemeItemToChallengeOrder(item_id=item_id,
                                                                    demand_or_order_id=demand_or_order_id,
                                                                    create_time=int(time.time()),
                                                                    upload_invoke_src=1,
                                                                    core_user_id=core_user_id, check_aweme=False,
                                                                    platform_channel=0
                                                                    )

    def audit_item(self, inner_pass=1, micro_app_pass=1, security_pass=1, ecom_pass=1, item_id=None):
        """
        mock审核视频结果, inner_pass 为星图专审队列审核结果，micro_app_pass为小程序侧审核结果，security_pass为抖音安全初审结果。
        传递1为pass, 0 为fail, 其他数为暂不添加审核结果
        :param inner_pass:
        :param micro_app_pass:
        :param security_pass:
        :return:
        """
        logging.info('in process: audit_item to pass...')
        audit_type_bits = self.challenge.audit_type_bits
        filters = {'challenge_id': self.challenge_id}
        if item_id:
            filters.update(**{'item_id': item_id})
        self.item_stats = ChallengeItemStatDAL.query(filters)

        for i, item_stat in enumerate(self.item_stats):
            logging.info('process item: %s', item_stat.item_id)
            # refer: star_generic/business/tcs_internal/douyin_contribute_articles_audit_v2.py
            challenge_client.InnerChallengeTcsAuditResultSave(item_id=item_stat.item_id,
                                                              tcs_value=1 if inner_pass else -1,
                                                              content_tcs_value=1 if inner_pass else -1,
                                                              relevant_tcs_value=1 if inner_pass else -1,
                                                              anchor_relevant_tcs_value=1,
                                                              show_reason={})
            # refer: star_faas/ad.star_faas.microapp_star_atlas_rsp/index.py
            if audit_type_bits & 32:
                challenge_client.InnerSetChallengeMicroappAuditResult(item_id=item_stat.item_id,
                                                                      audit_result=1 if micro_app_pass else 2,
                                                                      reject_reason='' if micro_app_pass else '测试小程序审核失败')

            # refer: star_faas/ad.star_faas.common_processor/index.py
            if audit_type_bits & 8:
                challenge_client.InnerSetChallengeItemAudit(item_id=item_stat.item_id,
                                                            platform_channel=1,
                                                            audit_result_items=[{
                                                                "audit_type": 3,
                                                                "audit_value": 1 if security_pass else -1,
                                                                "audit_source": 'aweme_challenge_audit',
                                                                "reason": "" if security_pass else '抖音安全初审不通过',
                                                            }])

            # refer: star_kafka/processors/star_ecom_product_audit_processor.py
            if audit_type_bits & 128:
                challenge_client.InnerSetChallengeItemAudit(item_id=item_stat.item_id,
                                                            platform_channel=1,
                                                            audit_result_items=[{"audit_type": 7,
                                                                                 "audit_value": 1 if ecom_pass else -1,
                                                                                 "audit_source": 'ecom',
                                                                                 "reason": '' if ecom_pass else '电商侧审核不通过'}])

    def gen_convert_stat(self):
        self._mock_convert_stat()
        self._mock_item_cost()

    def _mock_convert_stat(self):
        logging.info('in process: mock_convert_stat')
        self.item_stats = ChallengeItemStatDAL.query({'challenge_id': self.challenge_id})
        for i, stat in enumerate(self.item_stats):
            for j in range(self.delta.days):
                share_vv = 0
                if challenge.pay_type == ChallengePayType.cpm.value:
                    share_vv = j * 50
                ChallengeStatDAL.new(challenge_id=self.challenge_id,
                                     sync_date=self.challenge.expiration_time + datetime.timedelta(days=j),
                                     user_id=stat.user_id, play=j * 100 + 5,
                                     like_cnt=j * 20 + 1, comment=j * 10 + 3,
                                     share=j * 3, share_vv=share_vv)

    def _mock_item_cost(self):
        logging.info('in process: _mock_item_cost. Default action: skip any action.')

    def mock_choose_reward(self):
        logging.info('in process: mock_choose_reward. Default action: skip any action.')

    def mock_challenge_bulletin_status(self):
        logging.info('in process: mock_challenge_bulletin_status. \n'
                     'Default action: update challenge status to 3 and audit status to 5.')
        self.challenge.update(status=ChallengeStatus.bulletin.value,
                              audit_status=ChallengeAuditStatus.no_need.value)

    def mock_challenge_reward_and_bulletin(self):
        logging.info('in process: mock_challenge_reward_and_bulletin. \n'
                     'Default action: execute [%s]' % self.choose_hander)
        self.choose_hander(EasyDict(challenge_id=self.challenge_id), True).process()

    def mock_challenge_wait_send_reward(self):
        logging.info('in process: mock_challenge_wait_send_reward. \n'
                     'Default action: update challenge status to 4 and audit status to 3.')
        self.challenge.update(status=ChallengeStatus.finished.value,
                              audit_status=ChallengeAuditStatus.process.value)

    def mock_challenge_send_reward(self):
        logging.info('in process: mock_cpm_challenge_send_reward.\n'
                     'Default action: execute [AdminSendChallengeRewardHandler].')
        AdminSendChallengeRewardHandler(EasyDict(challenge_id=self.challenge_id)).async_process()

    def clear_up(self):
        logging.info('in process: revert item occupation status.\n'
                     'Default action: update challenge status to 10.')
        self.challenge.update(**{'status': ChallengeStatus.closed.value})


class MockCps(MockBase):
    def __init__(self, challenge_id, env='prod'):
        super(MockCps, self).__init__(challenge_id, ChooseChallengeItemCpsHandler, env)

    def _mock_item_cost(self):
        logging.info('in process: mock_cps_item_cost')
        self.item_stats = ChallengeItemStatDAL.query({'challenge_id': self.challenge_id})
        self.author_id_item_stats = defaultdict(list)
        for item_stat in self.item_stats:
            self.author_id_item_stats[item_stat.user_id].append(item_stat)
        for i, item_stats in enumerate(self.author_id_item_stats.values()):
            budget = [self.budgets_for_users[i] * x / 100 for x in get_random(len(item_stats))]
            for _, item_stat in enumerate(item_stats):
                logging.info('process item: %s', item_stat.item_id)
                total_collect_count, total_sales = budget[_] / 10, budget[_]
                for j in range(self.delta.days):
                    stat_date = self.challenge.expiration_time + datetime.timedelta(days=j)
                    sales = total_sales * (j + 1) / self.delta.days
                    StarItemCostDailyDAL.new(challenge_id=self.challenge_id, item_id=item_stat.item_id,
                                             user_id=item_stat.user_id,
                                             core_user_id=item_stat.core_user_id,
                                             item_cost=10000 * sales,
                                             stat_date=stat_date)
                item_stat.update(collect_count=total_collect_count, sales=total_sales)


class MockCpsNew(MockBase):
    def __init__(self, challenge_id, env='prod'):
        super(MockCpsNew, self).__init__(challenge_id, ChooseChallengeItemCpsHandler, env)

    def _mock_item_cost(self):
        logging.info('in process: mock_cps_new_item_cost')
        self.item_stats = ChallengeItemStatDAL.query({'challenge_id': self.challenge_id})
        self.author_id_item_stats = defaultdict(list)
        for item_stat in self.item_stats:
            self.author_id_item_stats[item_stat.user_id].append(item_stat)
        for i, item_stats in enumerate(self.author_id_item_stats.values()):
            budget = [self.budgets_for_users[i] * x / 100 for x in get_random(len(item_stats))]
            for _, item_stat in enumerate(item_stats):
                logging.info('process item: %s', item_stat.item_id)

                total_paid_num, total_confirmed_num, total_confirmed_amount = budget[_] + random.randint(10, 100), \
                                                                              budget[_] / 10, budget[_]

                for j in range(self.delta.days):  # 写入每天的消耗数据
                    stat_date = self.challenge.expiration_time + datetime.timedelta(days=j)
                    paid_num = int(total_paid_num * (j + 1) / self.delta.days)
                    confirmed_num = int(total_confirmed_num * (j + 1) / self.delta.days)
                    confirmed_amout = int(total_confirmed_amount * (j + 1) / self.delta.days)

                    StarItemCostDailyDAL.new(challenge_id=self.challenge_id, item_id=item_stat.item_id,
                                             user_id=item_stat.user_id,
                                             core_user_id=item_stat.core_user_id,
                                             cost_type=CostType.coupon.value,
                                             cost_stat=json.dumps({'PaidNum': paid_num, 'ConfirmedNum': confirmed_num}),
                                             item_cost=confirmed_amout * 10000,
                                             stat_date=stat_date)
                for attribute, int_value in {1: total_paid_num, 2: total_confirmed_num}.items():
                    extra_info = StarChallengeItemExtraInfoDAL.query_one(
                        {'challenge_id': self.challenge_id, 'item_id': item_stat.item_id, 'attribute': attribute})
                    if extra_info:
                        extra_info.update(int_value=int_value)
                    else:
                        StarChallengeItemExtraInfoDAL.new(challenge_id=self.challenge_id, item_id=item_stat.item_id,
                                                          user_id=item_stat.user_id,
                                                          attribute=attribute, int_value=int_value)


class MockCpm(MockBase):
    def __init__(self, challenge_id, env='prod'):
        super(MockCpm, self).__init__(challenge_id, ChooseChallengeItemCpmHandler, env)

    def _mock_item_cost(self):
        logging.info('in process: mock_cpm_item_cost')
        self.item_stats = ChallengeItemStatDAL.query({'challenge_id': self.challenge_id})
        self.author_id_item_stats = defaultdict(list)
        for item_stat in self.item_stats:
            self.author_id_item_stats[item_stat.user_id].append(item_stat)
        for i, item_stats in enumerate(self.author_id_item_stats.values()):
            budget = [self.budgets_for_users[i] * x / 100 for x in get_random(len(item_stats))]
            for _, item_stat in enumerate(item_stats):
                logging.info('process item: %s', item_stat.item_id)
                total_share_vv = int(budget[_]) * 100  # 按cpm 10估，播放量为预算的100倍
                share_vv_each_day = get_random(self.delta.days, total_share_vv)
                item_cost_total = 0
                for j in range(self.delta.days):
                    stat_date = self.challenge.expiration_time + datetime.timedelta(days=j)
                    logging.info('processing item:date: %s:%s', item_stat.item_id, stat_date)
                    item_cost = 100 * share_vv_each_day[j]
                    item_cost_total += item_cost
                    share_vvs = {'share_vv': share_vv_each_day[j]}
                    StarItemCostDailyDAL.new(challenge_id=self.challenge_id, item_id=item_stat.item_id,
                                             core_user_id=item_stat.core_user_id,
                                             user_id=item_stat.user_id,
                                             item_cost=item_cost_total,
                                             cost_stat=json.dumps(share_vvs),
                                             cost_type=CostType.cpm.value,
                                             stat_date=stat_date)
                item_stat.update(share_vv=total_share_vv)


class MockCpa(MockBase):
    def __init__(self, challenge_id, env='prod'):
        super(MockCpa, self).__init__(challenge_id, ChooseChallengeItemCpaHandler, env)

    def _mock_item_cost(self):
        logging.info('in process: mock_cpa_item_cost')
        self.item_stats = ChallengeItemStatDAL.query({'challenge_id': self.challenge_id})
        self.author_id_item_stats = defaultdict(list)
        for item_stat in self.item_stats:
            self.author_id_item_stats[item_stat.user_id].append(item_stat)
        for i, item_stats in enumerate(self.author_id_item_stats.values()):
            budget = [self.budgets_for_users[i] * x / 100 for x in get_random(len(item_stats))]
            for _, item_stat in enumerate(item_stats):
                logging.info('process item: %s', item_stat.item_id)

                total_lead_count = int(budget[_] * 1000 / self.challenge.convert_unit_amount)
                lead_count_each_day = get_random(self.delta.days, total_lead_count, return_float=False)
                for j in range(self.delta.days):
                    for x in range(lead_count_each_day[j]):
                        ConvertDetailDAL.new(**{
                            'convert_id': [challenge.ios_convert_id, challenge.android_convert_id][self.delta.days % 2],
                            'item_id': item_stat.item_id,
                            'obj_id': self.challenge_id,
                            'convert_time': get_today_zero_clock() - datetime.timedelta(j + 1) + datetime.timedelta(
                                hours=x % 24),
                            'source': 'homepage_hot' if x % 4 <= 2 else 'other'
                        })
                item_stat.update(convert_count=total_lead_count, ios_convert_count=total_lead_count / 2,
                                 android_convert_count=total_lead_count - total_lead_count / 2)


class MockLevelReward(MockBase):
    def __init__(self, challenge_id, env='prod'):
        super(MockLevelReward, self).__init__(challenge_id, None, env)

    def mock_choose_reward(self):
        logging.info('in process: mock_choose_reward. \n'
                     'MockLevelReward Action: update challenge status to 2 and audit_status to 5.')

        self.challenge.update(status=ChallengeStatus.choose_reward.value,
                              audit_status=ChallengeAuditStatus.no_need.value)

    def mock_challenge_bulletin_status(self):
        logging.info('in process: mock_challenge_bulletin_status. \n'
                     'MockLevelReward Action: skip any action.')

    def mock_challenge_reward_and_bulletin(self):
        logging.info('in process: mock_challenge_reward_and_bulletin. \n'
                     'MockLevelReward Action:  choose reward item for each level. Execute: [ChooseChallengeItem].')
        user_id = 6594597963010408461
        rewards = ChallengeRewardDAL.query({'challenge_id': self.challenge_id})
        reward_id_item_ids_pairs = [(rewards[0].id, [6916428281394810120]),
                                    (rewards[1].id, [6916426650108300557]),
                                    (rewards[2].id, [6916408700441840910]),
                                    ]
        params = dict(
            dev_user_id=user_id,
            service_name='challenge.AdStarChallengeService',
            service_method='ChooseChallengeItem',
            ignore_sign=True,
            challenge_id=str(self.challenge_id),
            reward_items=[{'reward_id': str(pair[0]), "item_ids": pair[1]}
                          for pair in reward_id_item_ids_pairs]
        )
        print params
        response = requests.post('http://star-boe.toutiao.com/h/api/gateway/handler_post/', json=params,
                                 headers={'x-tt-env': self.env, 'x-use-boe': '1',
                                          'Host': 'star-boe.toutiao.com'})
        print response.json()


class MockCustomReward(MockBase):
    def __init__(self, challenge_id, env='prod'):
        super(MockCustomReward, self).__init__(challenge_id, ChooseChallengeItemWithoutRewardHandler, env)

    def mock_choose_reward(self):
        logging.info('in process: mock_choose_reward. \n'
                     'MockCustomReward Action: update challenge status to 2 and audit_status to 5.')
        self.challenge.update(status=ChallengeStatus.choose_reward.value,
                              audit_status=ChallengeAuditStatus.no_need.value)

    def mock_challenge_bulletin_status(self):
        logging.info('in process: mock_challenge_bulletin_status.\n'
                     'MockCustomReward Action: skip any action.')

    def mock_challenge_reward_and_bulletin(self):
        logging.info('in process: mock_challenge_reward_and_bulletin.\n'
                     'MockCustomReward Action: choose the reward item. Execute: ChooseChallengeItemWithoutReward.')
        item_id_reward_amount_dict = {
            6916428281394793736: 4000000,
            6916426650108398861: 3000000,
            6916425781572799757: 2000000
        }
        params = dict(
            challenge_id=self.challenge_id,
            item_rewards=[{'item_id': item_id, 'reward_amount': reward_amount} for item_id, reward_amount
                          in (item_id_reward_amount_dict or {}).items()],
            dev_user_id=6594597963010408461,
            service_name='challenge.AdStarChallengeService',
            service_method='ChooseChallengeItemWithoutReward',
            ignore_sign=True,
        )
        response = requests.post('http://star-boe.toutiao.com/h/api/gateway/handler_post/', json=params,
                                 headers={'x-tt-env': self.env, 'x-use-boe': '1',
                                          'Host': 'star-boe.toutiao.com'}
                                 )
        print response.json()


class MockAdIncome(MockBase):
    def __init__(self, challenge_id, env='prod'):
        super(MockAdIncome, self).__init__(challenge_id, ChooseChallengeItemAdIncomeHandler, env)

    def _mock_item_cost(self):
        raise Exception('CANNOT mock now, see star_orders/scripts/sync_challenge_ad_income_stat.py for detail.')


class MockSecretCpa(MockBase):
    def __init__(self, challenge_id, env='prod'):
        super(MockSecretCpa, self).__init__(challenge_id, ChooseChallengeItemSecretCpaHandler, env)

    def _mock_item_cost(self):
        logging.info('in process: mock secret_cpa item cost...')
        self.item_stats = ChallengeItemStatDAL.query({'challenge_id': self.challenge_id})
        self.author_id_item_stats = defaultdict(list)
        for item_stat in self.item_stats:
            self.author_id_item_stats[item_stat.user_id].append(item_stat)
        for i, item_stats in enumerate(self.author_id_item_stats.values()):
            budget = [self.budgets_for_users[i] * x / 100 for x in get_random(len(item_stats))]
            for _, item_stat in enumerate(item_stats):
                logging.info('process item: %s', item_stat.item_id)
                # mock lead count
                total_lead_count = int(budget[_] * 1000 / self.challenge.convert_unit_amount)
                lead_count_each_day = get_random(self.delta.days, total_lead_count, return_float=False)

                # mock valid share vv
                total_share_vv = int(budget[_]) * 100  # 按cpm 10估，播放量为预算的100倍
                share_vv_each_day = get_random(self.delta.days, total_share_vv)
                item_cost_total = 0
                for j in range(self.delta.days):
                    stat_date = self.challenge.expiration_time + datetime.timedelta(days=j)
                    logging.info('processing item:date: %s:%s', item_stat.item_id, stat_date)
                    item_cost = 100 * share_vv_each_day[j]
                    item_cost_total += item_cost
                    share_vvs = {'share_vv': int(share_vv_each_day[j])}

                    # mock share vv each day
                    StarItemCostDailyDAL.new(challenge_id=self.challenge_id, item_id=item_stat.item_id,
                                             core_user_id=item_stat.core_user_id,
                                             user_id=item_stat.user_id,
                                             item_cost=item_cost_total,
                                             cost_stat=json.dumps(share_vvs),
                                             cost_type=CostType.cpm.value,
                                             stat_date=stat_date)

                    # mock valid vv for each day
                    record = StarChallengeItemValidVVDAL.query_one(
                        {'item_id': item_stat.item_id, 'stat_date': stat_date})
                    if record:
                        record.update(vv=share_vv_each_day[j] + 300, used_vv=share_vv_each_day[j], )
                    else:
                        StarChallengeItemValidVVDAL.new(
                            item_id=item_stat.item_id,
                            core_user_id=item_stat.core_user_id,
                            vv=share_vv_each_day[j] + 300,
                            used_vv=share_vv_each_day[j],
                            stat_date=stat_date
                        )

                    # mock detail convert data for each day
                    for x in range(lead_count_each_day[j]):
                        ConvertDetailDAL.new(**{
                            'convert_id': [challenge.ios_convert_id, challenge.android_convert_id][self.delta.days % 2],
                            'item_id': item_stat.item_id,
                            'obj_id': self.challenge_id,
                            'convert_time': get_today_zero_clock() - datetime.timedelta(j + 1) + datetime.timedelta(
                                hours=x % 24),
                            'source': 'homepage_hot' if x % 4 <= 2 else 'other',
                            'event': 'active' if self.challenge.evaluate_type == 6 else 'download',
                            'os': 'android',
                            'is_fraud_rick_control': 2,
                            'is_match': 0.
                        })

                item_stat.update(convert_count=total_lead_count,
                                 ios_convert_count=total_lead_count / 2,
                                 android_convert_count=total_lead_count - total_lead_count / 2,
                                 share_vv=total_share_vv)


def parse():
    parser = argparse.ArgumentParser(prog='python create.py')
    parser.add_argument('challenge_id',
                        type=int,
                        help="投稿任务id")
    parser.add_argument('action', help='执行的动作.')
    parser.add_argument('-e', '--env', help='泳道标识', default='prod')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse()
    challenge_id = int(args.challenge_id)
    action = int(args.action)
    env = args.env

    challenge = ChallengeDAL.query_by_id(challenge_id)
    pay_type_mock_map = {
        ChallengePayType.cpm.value: MockCpm,
        ChallengePayType.convert.value: MockCpa,
        ChallengePayType.cps.value: MockCps,
        ChallengePayType.reward.value: MockLevelReward,
        ChallengePayType.custom.value: MockCustomReward,
        ChallengePayType.ad_income.value: MockAdIncome,
        ChallengePayType.coupon.value: MockCpsNew,  # 团购核销量结算
        ChallengePayType.secret_cpa.value: MockSecretCpa,  # cpa暗投cpm

    }
    mock = pay_type_mock_map[challenge.pay_type](challenge_id, env=env)
    mock.main(action)
