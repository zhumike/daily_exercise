# -*- coding: utf-8 -*-
'''
@Author : zhuzhenzhong
@File : demander_grade_update.py
'''

# coding: utf-8
import datetime
import sys
import time
import traceback


sys.path.insert(0, "/opt/tiger/ss_ad/ad_site_env/lib/python2.7/site-packages")
sys.path.insert(0, "/opt/tiger/toutiao/app/ad")
sys.path.insert(0, "/opt/tiger/toutiao/lib")
sys.path.insert(0, "/opt/tiger/toutiao/lib/frame")

sys.path.insert(0, "/home/liangjingwen.1252987/repos/toutiao/app/ad")
sys.path.insert(0, "/home/liangjingwen.1252987/repos/toutiao/lib")
sys.path.insert(0, "/home/liangjingwen.1252987/repos/toutiao/lib/frame")

from star_core.abase.client import AbaseRecord
from collections import defaultdict
from frame import logger as logging
from star_common.models.abase.demander_statics import DemanderCostStatAbase
from star_common.const.user.type import UserRole
from star_common.const.const import OrderSnapshotBillType
from star_common.dals.user import StarUserDAL
from star_common.dals.order import StarOrderBillSnapshotDAL, StarOrderDAL
from star_demander.business.demander_grade import DemanderGradeService
from star_common.utils.query_db import query_db_with_batch
from star_common.dals.demander_info import StarDemanderInformationDAL
from star_common.storage.db_session import supplier_read_only
from star_demander.business.demander_grade import DemanderGradeService


def  update_demander_update(test_demander,test_grade):
    user_id = test_demander
    valid_time = '2026-01-01 12:00:00'
    service = DemanderGradeService(user_id)
    valid_time = time.mktime(datetime.datetime.strptime(valid_time, '%Y-%m-%d %H:%M:%S').timetuple())
    service.reset_abase_data(new_grade=test_grade, grade_valid_time=valid_time)
    service.demander.update(demander_grade=test_grade)


if __name__ == "__main__":
    demander_id = sys.argv[1]
    new_grade = sys.argv[2]
    update_demander_update(demander_id,new_grade)