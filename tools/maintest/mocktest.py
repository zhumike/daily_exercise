# -*- coding: utf-8 -*-
# @Time : 2021/7/19 3:44 下午
# @Author : zhuzhenzhong

def mock_cpm_item_cost(challenge_id, cpm_strategy):
    """
    :param challenge_id:
    :param cpm_strategy: CpmStrategy
    :return:
    """
    challenge = ChallengeDAL.query_by_id(challenge_id)
    item_stats = ChallengeItemStatDAL.query({'challenge_id': challenge_id, 'total_tcs_value': 1})
    if not item_stats:
        return
    expiration_time = challenge.expiration_time.date()
    expiration_time_end = challenge.expiration_time_end.date()
    delta = expiration_time_end - expiration_time
    days = min(delta.days, cpm_strategy.days)
    for i, item_stat in enumerate(item_stats):
        total_share_vv = cpm_strategy.total_vv/len(item_stats)

        if i == len(item_stats) - 1:
            item_cost_total = cpm_strategy.total_cost - cpm_strategy.total_cost / len(item_stats) * i
        else:
            item_cost_total = cpm_strategy.total_cost/len(item_stats)
        current_total = 0
        for j in range(days):
            stat_date = expiration_time + datetime.timedelta(days=j)
            vv = total_share_vv / days
            item_cost = item_cost_total/days
            if j == days - 1:
                current_total = item_cost_total
            else:
                current_total += item_cost
            share_vvs = {'share_vv': vv}
            StarItemCostDailyDAL.new(challenge_id=challenge_id, item_id=item_stat.item_id,
                                     core_user_id=item_stat.core_user_id,
                                     user_id=item_stat.user_id,
                                     item_cost=current_total,
                                     cost_stat=json.dumps(share_vvs),
                                     cost_type=CostType.cpm.value,
                                     stat_date=stat_date)
        item_stat.update(share_vv=total_share_vv)

cpm_strategy=CpmStrategy(total_cost_yuan=0, total_vv=1000000)