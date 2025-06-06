# coding=utf-8

import sys
import datetime
import os

os.environ['SERVICE_MESH_EGRESS_ADDR'] = '/opt/tiger/toutiao/var/service/%s.mesh/rpc.egress.sock' % os.getenv('TCE_PSM')

sys.path.append('/opt/tiger/toutiao/app/ad')
sys.path.append('/home/zhoufengshun/repos/toutiao/app/ad/star_rpc/')
sys.path.append('/opt/tiger/ad/data')


def test(s1,s2):
    from star_common.gateway.base_rpc import generic_client

    star_id = s1
    if  isinstance(s2,str):
        pass
    else:
        s2 = str(s2)
    open_id = s2
    generic_client.InnerBindWechatOpenId(open_id=open_id, system_type=2, is_bind=1, star_id=star_id)
    print "finish"

if __name__ == '__main__':
    star_id = sys.argv[1]
    open_id = sys.argv[2]
    test(star_id,open_id)