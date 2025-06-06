# -*- coding: utf-8 -*-
# @Time : 2022/9/5 10:51 上午
# @Author : zhuzhenzhong
# coding: utf-8
import sys

sys.path.insert(0, "/opt/tiger/ss_ad/ad_site_env/lib/python2.7/site-packages")
sys.path.insert(0, "/opt/tiger/toutiao/app/ad")
sys.path.insert(0, "/opt/tiger/toutiao/lib")
sys.path.insert(0, "/opt/tiger/toutiao/lib/frame")
sys.path.append('/opt/tiger/')
sys.path.insert(0, '/opt/tiger/toutiao/webarch_lib')

from star_common.dals.author_extra_info import StarAuthorExtraInfoIntDAL
from star_common.dals.credit_score import StarCreditScoreDAL


#change_score--改变后的期望的分数       change_score--想要增加的分数     author_id--星图达人id
#在author服务中运行。

if __name__ == '__main__':
    StarCreditScoreDAL.new(author_id=6946461064036876302, change_score=50, change_reason=u"qa账号",
                           reason_category=u'内部账号豁免', score=100)
    record = StarAuthorExtraInfoIntDAL.query_one(
        {'author_id': 6946461064036876302, 'attribute': "credit_score_punish_time", 'platform_source': 0})
    record.update(int_value=1661702400)