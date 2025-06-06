#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# import lib
# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# import lib
import sys
import traceback



sys.path.insert(0, '/opt/tiger/ss_ad/ad_site_env/lib/python2.7/site-packages')
sys.path.insert(0, '/opt/tiger/')
sys.path.insert(0, '/opt/tiger/toutiao/app/ad')
sys.path.insert(0, '/opt/tiger/toutiao/webarch_lib')
sys.path.insert(0, '/opt/tiger/toutiao/app/ad/star_orders')
import json
import time
from datetime import datetime
from star_orders.business.campaign.industry_ensure_campaign.campiagn_item_info import CampaignItemInfo
from star_common.dals.campaign import StarCampaignDAL
from star_common.dals.demand import StarDemandDAL
from star_common.dals.order import StarOrderDAL
from frame import logger as logging

from star_common.gateway.base_rpc import challenge_client

from star_orders.ad_star_orders import AdminChallengeAuditReq
from business.payment.campaign_payment_business import CampaignPaymentBusiness
from star_common.storage.redis_star_cli import Lock
from star_orders.business.challenge.challenge_admin import AdminChallengeAuditHandler
from star_orders.const.challenge import ChallengeAuditStatus


class CampaignAutoProcessHandler(object):
    def __init__(self, campaign_id, is_vv_valid=False, skip_ongoing_task_check=False):
        self.campaign_id = campaign_id
        self.challenge_data = {}
        self.campaign = None
        self.demand = None
        self.challenge_id = 0
        self.release_user_id = None

        self.expiration_time = int(time.mktime(datetime.now().timetuple()))
        self.expiration_time_end = int(time.mktime(datetime.now().timetuple()))
        self.content_requirement = []
        self.challenge_budget = 0
        self.total_pay = None
        self.demand_data = None
        self.campaign_current_freeze_amount = 0
        self.challenge_demand_id = 0
        self.skip_ongoing_task = skip_ongoing_task_check
        self.is_vv_valid = is_vv_valid
        self.industry_ensure_deadline = 0

    def monitor(self, stage="", err_info=""):
        """
        :return: 监控任务流程
        """
        logging.error("=" * 100)
        logging.error("campaign星选套餐，保量定时任务异常。campaign_id=%s, [%s] 阶段出错, 错误栈: %s" % (self.campaign_id, stage, err_info))
        logging.error("=" * 100)
        return

    def check_campaign_basic_status(self):
        self.campaign = StarCampaignDAL.query_by_id(self.campaign_id)
        if not self.campaign:
            return False
        self.release_user_id = self.campaign.release_user_id
        campaign_data = self.campaign.data
        if campaign_data.get("industry_ensure_status") != 1:
            logging.info(
                "campaign_id= {} 保量状态不对, 无法发单".format(self.campaign_id, campaign_data.get("industry_ensure_status")))
            return False
        if campaign_data.get("industry_ensure_task_id") > 0 or campaign_data.get("industry_ensure_status") != 1:
            logging.info("campaign_id= {} 已经产生保量投稿任务, 任务ID:{} 无法再次保量".format(self.campaign_id, campaign_data.get(
                "industry_ensure_task_id")))
            return False
        self.demand = StarDemandDAL.query_one(equal_filters={'campaign_id': self.campaign_id, 'task_category': 1})
        if not self.demand:
            return False
        self.campaign_current_freeze_amount = self.campaign.data.get('current_freeze_amount')
        if self.campaign_current_freeze_amount < 0:
            logging.info("campaign_id=%s 当前没有可以使用的金额用于保量任务", self.campaign_id)
            return False
        return True

    def check_producer_order_items(self):
        """
           校验所有有效订单都处于视频发布三天后的状态
        """
        demand_id = self.demand
        no_publish_valid_orders = StarOrderDAL.query(
            equal_filters={'demand_id': demand_id, 'status__notin': [-3, -2, 2, 4, 54, 3]})
        if no_publish_valid_orders:
            no_publish_valid_order_ids = [_.id for _ in no_publish_valid_orders]
            logging.info("campaign_id = {}, 有进行中的订单: {}".format(self.campaign_id, no_publish_valid_order_ids))
            return False
        publish_in_three_days_orders = StarOrderDAL.query(
            equal_filters={'demand_id': demand_id, 'status__in': [54, 3], })
        if publish_in_three_days_orders:
            publish_in_three_days_order_ids = [_.id for _ in publish_in_three_days_orders]
            logging.info("campaign_id = {}, 有进行中的订单: {}".format(self.campaign_id, publish_in_three_days_order_ids))
            return False
        return True

    def check_campaign_vv_is_valid(self):
        """
        :return: 指派任务校验视频VV达标
        """
        if self.is_vv_valid:
            return True
        insure_info = self.campaign.data.get("insure_package_info")
        if not insure_info:
            raise
        insure_vv = insure_info.get('data').get("insure_vv")
        producer_demand_real_vv = CampaignItemInfo.get_producer_items_vv([self.demand.id]) or 0
        logging.info("指派任务校验视频VV达标 insure_vv=%s,  producer_demand_real_vv =%s" % (insure_vv, producer_demand_real_vv))
        return insure_vv <= producer_demand_real_vv

    def generate_challenge_data(self):
        logging.info("campaign_id=%s 开始构造投稿任务的发单数据", self.campaign_id)
        self.demand_data = self.demand.data
        content_requirement = json.loads(self.campaign.data.get("content_requirement", "[]"))
        for _ in content_requirement:
            _['content'] = str(_['content'])
        self.expiration_time = int(time.mktime(datetime.now().timetuple()))
        self.expiration_time_end = int(time.mktime(datetime.now().timetuple())) + 24 * 60 * 60 * 12
        self.industry_ensure_deadline = int(time.mktime(datetime.now().timetuple())) + 24 * 60 * 60 * 15
        self.content_requirement = content_requirement
        self.challenge_budget = 0
        self.total_pay = self.campaign_current_freeze_amount
        # 计算发单的价格信息 剩余的任务金额， 需要从服务费上分离出来
        if self.check_campaign_vv_is_valid():
            left_task_amount = max(int(round(self.total_pay / 1.05)) * 0.1, 10000)
        else:
            left_task_amount = int(round(self.total_pay / 1.05))
        self.challenge_budget = left_task_amount
        logging.info("campaign_id=%s 构造投稿任务的发单数据完毕", self.campaign_id)

    def create_challenge(self):
        logging.info("campaign_id=%s 投稿任务开始发单", self.campaign_id)
        createChallengeResp = challenge_client.InnerCreateChallenge(s_demander_id=self.release_user_id,
                                                                    campaign_id=self.campaign_id,
                                                                    total_pay_amount=self.total_pay * 1000,
                                                                    # 投稿的价格需要 * 1000
                                                                    product_name=str(
                                                                        self.demand_data.get('product_name', "")),
                                                                    first_class_category=self.demand.first_class_category,
                                                                    second_class_category=self.demand.second_class_category,
                                                                    expiration_time_end=self.expiration_time_end,
                                                                    product_information=str(
                                                                        self.demand_data.get('product_information',
                                                                                             "")),
                                                                    name=str(self.campaign.name),
                                                                    contact_id=self.demand.contact_id,
                                                                    other=json.dumps(
                                                                        {"content_advice_v2": self.content_requirement,
                                                                         "item_ids": []}),
                                                                    author_level_one_tags=[],
                                                                    author_level_two_tags=[],
                                                                    evaluate_type=5,  # 按播放量消耗
                                                                    evaluate_description="",
                                                                    author_scope=2,
                                                                    author_ids=[],
                                                                    challenge_type=1,
                                                                    max_publish_count=3,
                                                                    choose_reward_days=7,
                                                                    pay_type=4,  # cpm
                                                                    convert_unit_amount=0,
                                                                    budget=self.challenge_budget * 1000,
                                                                    adv_id=0,
                                                                    ios_convert_id=0,
                                                                    android_convert_id=0,
                                                                    max_follower=0,
                                                                    cpm_vv_price=0,
                                                                    demand_icon=self.campaign.data.get("campaign_icon",
                                                                                                       ""),
                                                                    max_reward=0,
                                                                    challenge_author_type=0,
                                                                    expiration_time=self.expiration_time,
                                                                    dispatch_auz=0,
                                                                    unit_amount_type=1,
                                                                    ios_convert_unit_amount=0,
                                                                    android_convert_unit_amount=0,
                                                                    challenge_sub_type=1,
                                                                    supply_sample=0,
                                                                    commission_rate=70,
                                                                    video_type=6,
                                                                    demand_source=1
                                                                    )
        self.challenge_demand_id = createChallengeResp.demand_id
        logging.info("Campaign_id = %s 保量投稿任务发单成功, 投稿总冻结金额: %s, 投稿任务预算: %s, challenge_demand_id: %s" % (
            self.campaign_id, self.total_pay, self.challenge_budget, self.challenge_demand_id))
        return

    def auto_audit_challenge(self):
        # 自动过审核
        try:
            req = AdminChallengeAuditReq(
                s_employee_id=0,
                challenge_id=self.challenge_demand_id,
                audit_status=ChallengeAuditStatus.passed.value
            )
            AdminChallengeAuditHandler(req).process()
            logging.info('投稿任务自动审核通过 %s', str(self.challenge_id))
            return
        except Exception as e:
            self.monitor(stage="投稿任务自动审核", err_info=traceback.format_exc())
            return

    def pre_create_challenge(self):
        """
        :return: 释放资金
        """
        try:
            logging.info("释放campaign冻结资金, 释放金额: %s", self.total_pay)
            CampaignPaymentBusiness.unfreeze_campaign_payment(self.release_user_id, self.campaign_id)
            logging.info("释放campaign冻结资金成功, 释放金额: %s", self.total_pay)
            return True
        except Exception as e:
            self.monitor(stage="解冻资金用于发单失败", err_info=traceback.format_exc())
            return False

    def after_create_challenge(self):
        """
        :return: 发单失败 重新冻结资金
        """
        retry_times = 1
        while retry_times <= 3:
            retry_times += 1
            try:
                logging.info("发单失败 重新冻结campaign资金, 冻结金额: %s", self.total_pay)
                CampaignPaymentBusiness.refreeze_campaign_payment(demander_id=self.release_user_id,
                                                                  campaign_id=self.campaign_id, amount=self.total_pay)
                return True
            except Exception as e:
                self.monitor(stage="投稿发单后，重新冻结campaign资金出错", err_info=traceback.format_exc())
        return False

    def _get_create_demand_redis_lock_key(self, s_demander_id):
        return "ad_star_create_demand:%s" % s_demander_id

    def update_campaign(self):
        campaign_data = self.campaign.data
        campaign_data.update({
            "current_freeze_amount": 0,
            "industry_ensure_status": 2,  # 保量阶段
            "industry_ensure_task_id": self.challenge_demand_id,
            "industry_ensure_deadline": self.industry_ensure_deadline,
        })
        logging.info("================  industry_ensure_deadline =%s " % self.industry_ensure_deadline)
        logging.info("======》  campaign_data = %s" % campaign_data)
        self.campaign.update(data=campaign_data)
        logging.info("======》  更新campaign的数据状态成功")

    def process(self):
        if not self.check_campaign_basic_status():
            logging.info("campaign_id=%s 不满足发单条件", self.campaign_id)
            return
        if not self.check_producer_order_items() and not self.skip_ongoing_task:
            logging.info("campaign_id=%s 有进行中的订单, 不满足发单条件", self.campaign_id)
            return
        logging.info("campaign_id=%s 构造投稿发单数据", self.campaign_id)
        with Lock(self._get_create_demand_redis_lock_key(self.release_user_id), blocking_timeout=0):
            self.generate_challenge_data()
            if not self.pre_create_challenge():
                return
            try:
                self.create_challenge()
            except Exception as e:
                logging.error("="*100)
                logging.error(traceback.format_exc())
                logging.error("=" * 100)
                self.after_create_challenge()
                return
            self.auto_audit_challenge()
            self.update_campaign()
        return


def test_process(campaign_id, is_vv_valid=True):
    """
    :return:  测试专用
    """
    skip_ongoing_task_check = True
    campaign = StarCampaignDAL.query_one(equal_filters={'id': campaign_id, 'status': 1, 'type': 1},
                                         order_by="id", column=['id', ])
    if not campaign:
        logging.info("campaign 不存在")
        return
    CampaignAutoProcessHandler(campaign.id, is_vv_valid=is_vv_valid,
                               skip_ongoing_task_check=skip_ongoing_task_check).process()


if __name__ == "__main__":
    campaign_id = sys.argv[1]
    is_vv = sys.argv[2]
    print campaign_id, is_vv
    test_process(campaign_id, is_vv_valid=True if is_vv == 1 else False)