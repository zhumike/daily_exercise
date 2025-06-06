# -*- coding: utf-8 -*-
# @Time : 2021/10/28 8:23 下午
# @Author : zhuzhenzhong

# coding=utf-8

import sys
import datetime
import os

os.environ['SERVICE_MESH_EGRESS_ADDR'] = '/opt/tiger/toutiao/var/service/%s.mesh/rpc.egress.sock' % os.getenv('TCE_PSM')

sys.path.append('/opt/tiger/toutiao/app/ad')
sys.path.append('/home/zhoufengshun/repos/toutiao/app/ad/star_rpc/')
sys.path.append('/opt/tiger/ad/data')


def test():
    from star_common.gateway.base_rpc import generic_client

    star_id = 1714663207131143
    open_id = 'oVbVs55yOWBUAWoMvVKXvLwrQ-Vg'
    generic_client.InnerBindWechatOpenId(open_id=open_id, system_type=2, is_bind=1, star_id=star_id)

    print "finish"

if __name__ == '__main__':
    test()