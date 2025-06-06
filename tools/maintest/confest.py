# -*- coding: utf-8 -*-
'''
@Author : zhuzhenzhong
@File : confest.py
'''


import os
import shutil
import json
import pytest
import logging
import platform
import allure
from euler.base_compat_middleware import gdpr_auth_middleware
from fratest.lib.event_track.eventcollect import EventCollecter

EventCollecter.set_collect_switch(False)
from lib import client

# 本机调试支持服务发现
if platform.system() == 'Darwin':
    os.environ['CONSUL_HTTP_HOST'] = '10.227.91.107'
    os.environ['CONSUL_HTTP_PORT'] = '2280'
    os.environ['RUNTIME_IDC_NAME'] = 'boe'
import time
from fratest.lib.thrift import base_middleware

from lib.db import qa_tables
from lib.common import get_file_fragment_author
from fratest.lib.thrift.send_thrift_request import *
from fratest.lib.get_service_info import *

from lib import rpc

cur_dir = os.path.dirname(os.path.abspath(__file__))
logger = logging.getLogger(__name__)


def default_call(self, ctx, req, *args, **kwargs):
    ret = ctx.next(req, *args, **kwargs)
    return ret


base_middleware.BaseMiddleware.__call__ = default_call


def pytest_addoption(parser):
    parser.addoption('--server-address', help='server host ip and port, e.q. "127.0.0.1:80"')
    parser.addoption('--env-tag', help='env tag')
    parser.addoption('--cluster', help='cluster')
    parser.addoption('--psm', help='psm')
    parser.addoption('--ip', help='ip')
    parser.addoption('--port', help='port')
    parser.addoption('--branch', default='master', help='idl branch')


def pytest_collection_modifyitems(config, items):
    # PPE can not connect to ad_supplier_qa which deployed in BOE,
    # return when task executing in PPE
    atlas_cluster = os.getenv('atlas_cluster')
    if atlas_cluster == 'boe' or atlas_cluster is None:
        case_infos = {}
        for item in items:
            case_location = item.location
            case_file = case_location[0]
            case_name = case_location[2]
            case_lineno = get_case_lineno(case_file, case_location[1])
            if case_file not in case_infos:
                case_infos[case_file] = {}
                entries = qa_tables.case_info.query_eq(file=case_file)
                for entry in entries:
                    case_infos[entry.file][entry.name] = entry
            if case_file not in case_infos or case_name not in case_infos[case_file]:
                qa_tables.case_info.insert(file=case_file, name=case_name)
            else:
                entry = case_infos[case_file][case_name]
                item.add_marker(pytest.mark.skipif(entry.skipped, reason=str(entry.skip_reason)))
                item.add_marker(allure.description(f'author:{entry.author}'))
            if config:
                entry = case_infos[case_file][case_name]
                if not entry.author:
                    authors = get_file_fragment_author(case_file, case_lineno)
                    entry.update(author=json.dumps(authors), last_author=authors[0])





def get_case_lineno(file, start_lineno):
    with open(file) as fd:
        lines = [line.rstrip() for line in fd.readlines()]
    start_line = lines[start_lineno]
    indent = count_indent(start_line)
    cur_lineno = start_lineno + 1
    end_lineno = len(lines) - 1
    case_defined = False
    if start_line.lstrip().startswith('def '):
        case_defined = True
    while cur_lineno < len(lines):
        cur_line = lines[cur_lineno]
        if cur_line.lstrip().startswith('def ') and not case_defined:
            case_defined = True
            cur_lineno += 1
            continue
        if not cur_line or cur_line.lstrip().startswith('#'):
            cur_lineno += 1
            continue
        cur_indent = count_indent(cur_line)
        if cur_indent <= indent:
            end_lineno = cur_lineno - 1
            break
        cur_lineno += 1
    while not lines[end_lineno] or lines[end_lineno].lstrip().startswith('#') and end_lineno > start_lineno:
        end_lineno -= 1
    return [start_lineno + 1, end_lineno + 1]  # git line start with 1


def count_indent(line):
    return len(line) - len(line.lstrip())


@pytest.fixture(autouse=True)
def running_interval():
    """case执行间隔0.3s，防止打崩boe环境"""
    time.sleep(0.3)


@pytest.fixture(scope='session', autouse=True)
def rpc_env(pytestconfig):
    env_tag = pytestconfig.getoption('env_tag', 'prod')
    os.environ['RPC_ENV'] = env_tag


def get_server_address(psm, env_tag, cluster):
    if env_tag is None:
        env_tag = 'prod'
    env_config = {'env': env_tag}
    if cluster is not None:
        env_config['cluster'] = cluster
    hosts = GetServiceInfo(psm).get_specify_service_info(env_config)
    if not hosts and env_tag != 'prod':  # 环境不存在该服务，默认启用prod环境
        env_config = {'env': 'prod'}
        hosts = GetServiceInfo(psm).get_specify_service_info(env_config)
    ip = hosts[0]['Host']
    port = hosts[0]['Port']
    return ip, port


@pytest.fixture(scope='class')
def mcn_client(pytestconfig):
    env_tag = pytestconfig.getoption('env_tag')
    branch = pytestconfig.getoption('branch')
    return client.RPCClient(psm='ad.star.mcn',
                            idl_remote=f'https://code.byted.org/ad/star_thrift_gen/blob/{branch}/idl/mcn.thrift',
                            idl_local=os.path.join(rpc.idl_root, 'ad/star_thrift_gen/idl/mcn.thrift'),
                            service='AdStarMcnService',
                            env_tag=env_tag,
                            timeout=600000,
                            branch=branch)


@pytest.fixture(scope='function')
def challenge_client(pytestconfig):
    env_tag = pytestconfig.getoption('env_tag')
    branch = pytestconfig.getoption('branch')
    return client.RPCClient(psm='ad.star.challenge',
                            idl_remote=f'https://code.byted.org/ad/star_thrift_gen/blob/{branch}/idl/challenge.thrift',
                            idl_local=os.path.join(rpc.idl_root, 'ad/star_thrift_gen/idl/challenge.thrift'),
                            service='AdStarChallengeService',
                            branch=branch,
                            timeout=600000,
                            env_tag=env_tag)


@pytest.fixture(scope='function')
def platform_client(pytestconfig):
    env_tag = pytestconfig.getoption('env_tag')
    branch = pytestconfig.getoption('branch')
    return client.RPCClient(psm='ad.star.platform',
                            idl_remote=f'https://code.byted.org/cpputil/service_rpc_idl/blob/'
                                       f'{branch}/ad/star/platform.thrift',
                            idl_local=os.path.join(rpc.idl_root, 'cpputil/service_rpc_idl/ad/star/platform.thrift'),
                            service='AdStarPlatform',
                            branch=branch,
                            timeout=60000,
                            env_tag=env_tag)


@pytest.fixture(scope='class')
def goplatform_client(pytestconfig):
    env_tag = pytestconfig.getoption('env_tag')
    branch = pytestconfig.getoption('branch')
    return client.RPCClient(psm='ad.star.goplatform',
                            idl_remote=f'https://code.byted.org/cpputil/service_rpc_idl/blob/'
                                       f'{branch}/ad/star/goplatform.thrift',
                            idl_local=os.path.join(rpc.idl_root, 'cpputil/service_rpc_idl/ad/star/goplatform.thrift'),
                            service='AdStarGoplatformService',
                            branch=branch,
                            timeout=60000,
                            env_tag=env_tag)


@pytest.fixture(scope='function')
def saturn_client(pytestconfig):
    env_tag = pytestconfig.getoption('env_tag')
    branch = pytestconfig.getoption('branch')
    return client.RPCClient(psm='ad.site.saturn',
                            idl_remote=f'https://code.byted.org/cpputil/service_rpc_idl/blob/'
                                       f'{branch}/ad/star/saturn.thrift',
                            idl_local=os.path.join(rpc.idl_root, 'cpputil/service_rpc_idl/ad/star/saturn.thrift'),
                            service='AdSiteSaturn',
                            branch=branch,
                            env_tag=env_tag,
                            timeout=60000
                            )


@pytest.fixture(scope='class')
def aweme_live_client(pytestconfig):
    env_tag = pytestconfig.getoption('env_tag')
    branch = pytestconfig.getoption('branch')
    return client.RPCClient(psm='live.room.goroom',
                            idl_remote=f'https://code.byted.org/cpputil/service_rpc_idl/blob/'
                                       f'master/ies_live/room.thrift',
                            idl_local=os.path.join(rpc.idl_root, 'cpputil/service_rpc_idl/ies_live/room.thrift'),
                            service='IesRoomService',
                            branch=branch,
                            env_tag=env_tag,
                            timeout=60000
                            )


@pytest.fixture(scope='class')
def search_client(pytestconfig):
    env_tag = pytestconfig.getoption('env_tag')
    branch = pytestconfig.getoption('branch')
    return client.RPCClient(psm='ad.site.star_search',
                            idl_remote=f'https://code.byted.org/ad/star_thrift_gen/blob/{branch}/idl/search.thrift',
                            idl_local=os.path.join(rpc.idl_root, 'ad/star_thrift_gen/idl/search.thrift'),
                            service='AdStarSearch',
                            branch=branch,
                            timeout=100000,
                            env_tag=env_tag)


@pytest.fixture(scope='class')
def gosearch_client(pytestconfig):
    env_tag = pytestconfig.getoption('env_tag')
    branch = pytestconfig.getoption('branch')
    return client.RPCClient(psm='ad.star.gosearch',
                            idl_remote=f'https://code.byted.org/ad/star_thrift_gen/blob/{branch}/idl/go_search.thrift',
                            idl_local=os.path.join(rpc.idl_root, 'ad/star_thrift_gen/idl/go_search.thrift'),
                            service='AdStarGoSearchService',
                            branch=branch,
                            timeout=100000,
                            env_tag=env_tag)


@pytest.fixture(scope='function')
def settlement_client(pytestconfig):
    env_tag = pytestconfig.getoption('env_tag')
    branch = pytestconfig.getoption('branch')
    return client.RPCClient(psm='ad.star.settlement',
                            idl_remote=f'https://code.byted.org/ad/star_thrift_gen/blob/{branch}/idl/settlement.thrift',
                            idl_local=os.path.join(rpc.idl_root, 'ad/star_thrift_gen/idl/settlement.thrift'),
                            service='AdStarSettlementService',
                            branch=branch,
                            env_tag=env_tag)


@pytest.fixture(scope='function')
def creative_orders_client(pytestconfig):
    env_tag = pytestconfig.getoption('env_tag')
    branch = pytestconfig.getoption('branch')
    return client.RPCClient(psm='ad.star.creative_orders',
                            idl_remote=f'https://code.byted.org/ad/star_thrift_gen/blob/'
                                       f'{branch}/idl/creative_orders.thrift',
                            idl_local=os.path.join(rpc.idl_root, 'ad/star_thrift_gen/idl/creative_orders.thrift'),
                            service='AdStarCreativeOrdersService',
                            branch=branch,
                            env_tag=env_tag)


@pytest.fixture(scope='function')
def marketing_client(pytestconfig):
    env_tag = pytestconfig.getoption('env_tag')
    branch = pytestconfig.getoption('branch')
    return client.RPCClient(psm='ad.star.marketing',
                            idl_remote=f'https://code.byted.org/ad/star_thrift_gen/blob/{branch}/idl/marketing.thrift',
                            idl_local=os.path.join(rpc.idl_root, 'ad/star_thrift_gen/idl/marketing.thrift'),
                            service='AdStarMarketingService',
                            branch=branch,
                            env_tag=env_tag)


@pytest.fixture(scope='function')
def cg_openapi_thrift_client():
    return client.RPCClient(psm='cg.openapi.thrift',
                            idl_remote='https://code.byted.org/cpputil/service_rpc_idl/blob/'
                                       'master/cg/openapi/ad_star_openapi.thrift',
                            idl_local=os.path.join(rpc.idl_root,
                                                   'cpputil/service_rpc_idl/cg/openapi/ad_star_openapi.thrift'),
                            service='OpenApiService',
                            env_tag='prod'
                            )


@pytest.fixture(scope='function')
def task_client(pytestconfig):
    env_tag = pytestconfig.getoption('env_tag')
    branch = pytestconfig.getoption('branch')
    return client.RPCClient(psm='ad.star.task',
                            idl_remote=f'https://code.byted.org/ad/star_thrift_gen/blob/{branch}/idl/task.thrift',
                            idl_local=os.path.join(rpc.idl_root, 'ad/star_thrift_gen/idl/task.thrift'),
                            service='AdStarTaskService',
                            branch=branch,
                            env_tag=env_tag)


@pytest.fixture(scope='function')
def orders_client(pytestconfig):
    env_tag = pytestconfig.getoption('env_tag')
    branch = pytestconfig.getoption('branch')
    return client.RPCClient(psm='ad.star.orders',
                            idl_remote=f'https://code.byted.org/ad/star_thrift_gen/blob/{branch}/idl/orders.thrift',
                            idl_local=os.path.join(rpc.idl_root, 'ad/star_thrift_gen/idl/orders.thrift'),
                            service='AdStarOrdersService',
                            env_tag=env_tag,
                            branch=branch,
                            timeout=60000)


@pytest.fixture(scope='function')
def author_client(pytestconfig):
    env_tag = pytestconfig.getoption('env_tag')
    branch = pytestconfig.getoption('branch')
    return client.RPCClient(psm='ad.star.author',
                            idl_remote=f'https://code.byted.org/ad/star_thrift_gen/blob/{branch}/idl/author.thrift',
                            idl_local=os.path.join(rpc.idl_root, 'ad/star_thrift_gen/idl/author.thrift'),
                            service='AdStarAuthorService',
                            branch=branch,
                            env_tag=env_tag,
                            timeout=20000)


@pytest.fixture(scope='function')
def go_author_client(pytestconfig):
    env_tag = pytestconfig.getoption('env_tag')
    branch = pytestconfig.getoption('branch')
    return client.RPCClient(psm='ad.star.goauthor',
                            idl_remote=f'https://code.byted.org/ad/star_thrift_gen/blob/{branch}/idl/go_author.thrift',
                            idl_local=os.path.join(rpc.idl_root, 'ad/star_thrift_gen/idl/go_author.thrift'),
                            service='AdStarGoAuthorService',
                            branch=branch,
                            env_tag=env_tag)


@pytest.fixture(scope='function')
def touch_client(pytestconfig):
    env_tag = pytestconfig.getoption('env_tag')
    branch = pytestconfig.getoption('branch')
    return client.RPCClient(psm='ad.star.touch',
                            idl_remote=f'https://code.byted.org/ad/star_thrift_gen/blob/{branch}/idl/touch.thrift',
                            idl_local=os.path.join(rpc.idl_root, 'ad/star_thrift_gen/idl/touch.thrift'),
                            service='AdStarTouchService',
                            branch=branch,
                            env_tag=env_tag)


@pytest.fixture(scope='function')
def cg_passport_thrift_client(pytestconfig):
    return client.RPCClient(psm='cg.passport.thrift',
                            idl_remote='https://code.byted.org/cpputil/service_rpc_idl/blob/master/cg/passport.thrift',
                            idl_local=os.path.join(rpc.idl_root, 'cpputil/service_rpc_idl/cg/passport.thrift'),
                            service='CgPassportService',
                            env_tag='prod',
                            timeout=20000
                            )


@pytest.fixture(scope='session')
def go_demander_client(pytestconfig):
    env_tag = pytestconfig.getoption('env_tag')
    branch = pytestconfig.getoption('branch')
    return client.RPCClient(psm='ad.star.godemander',
                            idl_remote=f'https://code.byted.org/ad/star_thrift_gen/blob/'
                                       f'{branch}/idl/go_demander.thrift',
                            idl_local=os.path.join(rpc.idl_root, 'ad/star_thrift_gen/idl/go_demander.thrift'),
                            service='AdStarGoDemanderService',
                            branch=branch,
                            env_tag=env_tag,
                            timeout=20000)


@pytest.fixture(scope='session')
def vas_client(pytestconfig):
    env_tag = pytestconfig.getoption('env_tag')
    branch = pytestconfig.getoption('branch')
    return client.RPCClient(psm='ad.star.vas',
                            idl_remote=f'https://code.byted.org/ad/star_thrift_gen/blob/{branch}/idl/vas.thrift',
                            idl_local=os.path.join(rpc.idl_root, 'ad/star_thrift_gen/idl/vas.thrift'),
                            service='AdStarVasService',
                            branch=branch,
                            env_tag=env_tag,
                            timeout=20000)


@pytest.fixture(scope='function')
def demander_client(pytestconfig):
    env_tag = pytestconfig.getoption('env_tag')
    branch = pytestconfig.getoption('branch')
    return client.RPCClient(psm='ad.star.demander',
                            idl_remote=f'https://code.byted.org/ad/star_thrift_gen/blob/{branch}/idl/demander.thrift',
                            idl_local=os.path.join(rpc.idl_root, 'ad/star_thrift_gen/idl/demander.thrift'),
                            service='AdStarDemanderService',
                            branch=branch,
                            env_tag=env_tag,
                            timeout=20000)


@pytest.fixture(scope='function')
def generic_client(pytestconfig):
    env_tag = pytestconfig.getoption('env_tag')
    branch = pytestconfig.getoption('branch')
    return client.RPCClient(psm='ad.star.generic',
                            idl_remote=f'https://code.byted.org/ad/star_thrift_gen/blob/{branch}/idl/generic.thrift',
                            idl_local=os.path.join(rpc.idl_root, 'ad/star_thrift_gen/idl/generic.thrift'),
                            service='AdStarGenericService',
                            branch=branch,
                            env_tag=env_tag,
                            timeout=20000)


@pytest.fixture(scope='class')
def data_client(pytestconfig):
    env_tag = pytestconfig.getoption('env_tag')
    branch = pytestconfig.getoption('branch')
    return client.RPCClient(psm='ad.star.data',
                            idl_remote=f'https://code.byted.org/ad/star_thrift_gen/blob/{branch}/idl/data.thrift',
                            idl_local=os.path.join(rpc.idl_root, 'ad/star_thrift_gen/idl/data.thrift'),
                            service='AdStarDataService',
                            branch=branch,
                            env_tag=env_tag,
                            timeout=20000)


@pytest.fixture(scope='function')
def creative_coupon_client(pytestconfig):
    env_tag = pytestconfig.getoption('env_tag')
    branch = pytestconfig.getoption('branch')
    return client.RPCClient(psm='ad.star.creative_coupon',
                            idl_remote=f'https://code.byted.org/ad/star_thrift_gen/blob/'
                                       f'{branch}/idl/creative_coupon.thrift',
                            idl_local=os.path.join(rpc.idl_root, 'ad/star_thrift_gen/idl/creative_coupon.thrift'),
                            service='AdStarCreativeCouponService',
                            branch=branch,
                            env_tag=env_tag)


@pytest.fixture(scope='function')
def creative_materials_client(pytestconfig):
    env_tag = pytestconfig.getoption('env_tag')
    branch = pytestconfig.getoption('branch')
    return client.RPCClient(psm='ad.star.creative_materials',
                            idl_remote=f'https://code.byted.org/ad/star_thrift_gen/blob/'
                                       f'{branch}/idl/creative_materials.thrift',
                            idl_local=os.path.join(rpc.idl_root, 'ad/star_thrift_gen/idl/creative_materials.thrift'),
                            service='AdStarCreativeMaterialsService',
                            branch=branch,
                            env_tag=env_tag)


@pytest.fixture(scope='class')
def creative_demander_client(pytestconfig):
    env_tag = pytestconfig.getoption('env_tag')
    branch = pytestconfig.getoption('branch')
    return client.RPCClient(psm='ad.star.creative_demander',
                            idl_remote=f'https://code.byted.org/ad/star_thrift_gen/blob/'
                                       f'{branch}/idl/creative_demander.thrift',
                            idl_local=os.path.join(rpc.idl_root, 'ad/star_thrift_gen/idl/creative_demander.thrift'),
                            service='AdStarCreativeDemanderService',
                            branch=branch,
                            env_tag=env_tag)


@pytest.fixture(scope='class')
def creative_crm_client(pytestconfig):
    env_tag = pytestconfig.getoption('env_tag')
    branch = pytestconfig.getoption('branch')
    return client.RPCClient(psm='ad.star.creative_crm',
                            idl_remote=f'https://code.byted.org/ad/star_thrift_gen/blob/'
                                       f'{branch}/idl/creative_crm.thrift',
                            idl_local=os.path.join(rpc.idl_root, 'ad/star_thrift_gen/idl/creative_crm.thrift'),
                            service='AdStarCreativeCrmService',
                            branch=branch,
                            env_tag=env_tag)


@pytest.fixture(scope='class')
def creative_activity_client(pytestconfig):
    env_tag = pytestconfig.getoption('env_tag')
    branch = pytestconfig.getoption('branch')
    return client.RPCClient(psm='ad.star.creative_activity',
                            idl_remote=f'https://code.byted.org/ad/star_thrift_gen/blob/'
                                       f'{branch}/idl/creative_activity.thrift',
                            idl_local=os.path.join(rpc.idl_root, 'ad/star_thrift_gen/idl/creative_activity.thrift'),
                            service='AdStarCreativeActivityService',
                            branch=branch,
                            env_tag=env_tag)


@pytest.fixture(scope='function')
def community_client(pytestconfig):
    env_tag = pytestconfig.getoption('env_tag')
    branch = pytestconfig.getoption('branch')
    return client.RPCClient(psm='ad.star.community',
                            idl_remote=f'https://code.byted.org/cpputil/service_rpc_idl/blob/'
                                       f'{branch}/ad/star/community.thrift',
                            idl_local=os.path.join(rpc.idl_root, 'cpputil/service_rpc_idl/ad/star/community.thrift'),
                            service='AdStarCommunity',
                            branch=branch,
                            env_tag=env_tag,
                            timeout=20000)


@pytest.fixture(scope='function')
def audit_gateway_client(pytestconfig):
    env_tag = pytestconfig.getoption('env_tag')
    branch = pytestconfig.getoption('branch')
    return client.RPCClient(psm='ad.star.audit_gateway',
                            idl_remote=f'https://code.byted.org/ad/star_thrift_gen/blob/'
                                       f'{branch}/idl/audit_gateway.thrift',
                            idl_local=os.path.join(rpc.idl_root, 'ad/star_thrift_gen/idl/audit_gateway.thrift'),
                            service='AdStarAuditGatewayService',
                            branch=branch,
                            env_tag=env_tag)


@pytest.fixture(scope='function')
def caijing_tp_paycore_client(pytestconfig):
    env_tag = pytestconfig.getoption('env_tag')
    return client.RPCClient(psm='caijing.tp.paycore',
                            idl_remote=f'https://code.byted.org/caijing_pay/tp_paycore/blob/master/idl/paycore.thrift',
                            idl_local=os.path.join(rpc.idl_root, 'caijing_pay/tp_paycore/idl/paycore.thrift'),
                            service='PayCoreService',
                            env_tag=env_tag)


@pytest.fixture(scope='function')
def go_orders_client(pytestconfig):
    env_tag = pytestconfig.getoption('env_tag')
    branch = pytestconfig.getoption('branch')
    return client.RPCClient(psm='ad.star.goorders',
                            idl_remote=f'https://code.byted.org/ad/star_thrift_gen/blob/{branch}/idl/go_orders.thrift',
                            idl_local=os.path.join(rpc.idl_root, 'ad/star_thrift_gen/idl/go_orders.thrift'),
                            service='AdStarGoOrdersService',
                            branch=branch,
                            env_tag=env_tag,
                            timeout=20000)


@pytest.fixture(scope='class')
def control_client(pytestconfig):
    env_tag = pytestconfig.getoption('env_tag')
    branch = pytestconfig.getoption('branch')
    return client.RPCClient(psm='ad.star.control',
                            idl_remote=f'https://code.byted.org/ad/star_thrift_gen/blob/{branch}/idl/control.thrift',
                            idl_local=os.path.join(rpc.idl_root, 'ad/star_thrift_gen/idl/control.thrift'),
                            service='AdStarControlService',
                            branch=branch,
                            env_tag=env_tag)


@pytest.fixture(scope='function')
def gomcn_client(pytestconfig):
    env_tag = pytestconfig.getoption('env_tag')
    branch = pytestconfig.getoption('branch')
    return client.RPCClient(psm='ad.star.gomcn',
                            idl_remote=f'https://code.byted.org/ad/star_thrift_gen/blob/{branch}/idl/go_mcn.thrift',
                            idl_local=os.path.join(rpc.idl_root, 'ad/star_thrift_gen/idl/go_mcn.thrift'),
                            service='AdStarGoMcnService',
                            branch=branch,
                            env_tag=env_tag)


@pytest.fixture(scope='function')
def gouser_client(pytestconfig):
    env_tag = pytestconfig.getoption('env_tag')
    branch = pytestconfig.getoption('branch')
    return client.RPCClient(psm='ad.star.gouser',
                            idl_remote=f'https://code.byted.org/ad/star_thrift_gen/blob/{branch}/idl/go_user.thrift',
                            idl_local=os.path.join(rpc.idl_root, 'ad/star_thrift_gen/idl/go_user.thrift'),
                            service='AdStarGoUserService',
                            branch=branch,
                            env_tag=env_tag)

@pytest.fixture(scope='function')
def matrix_client(pytestconfig):
    psm = 'ad.star.matrix'
    rpc.update_idl('https://code.byted.org/ad/star_matrix/blob/master/idl/ad_star_matrix.thrift')
    ip = None
    port = None
    env_tag = pytestconfig.getoption('env_tag', 'prod')
    if env_tag.upper()[:3] == 'PPE':
        ip = pytestconfig.getoption('ip')
        port = int(pytestconfig.getoption('port'))
    elif env_tag is not None:
        env_config = {'env': env_tag}
        cluster = pytestconfig.getoption('cluster')
        if cluster is not None:
            env_config['cluster'] = cluster
        hosts = GetServiceInfo(psm).get_specify_service_info(env_config)
        if not hosts:  # 环境不存在该服务，默认启用prod环境
            env_config = {'env': 'prod'}
            hosts = GetServiceInfo(psm).get_specify_service_info(env_config)
        ip = hosts[0]['Host']
        port = hosts[0]['Port']
    logger.info('server address:{}:{}'.format(ip, port))
    idl_path = os.path.join(rpc.idl_root, 'ad/star_matrix/idl/ad_star_matrix.thrift')
    client = get_thrift_service_client(idl_path, 'AdStarMatrixService', ip, port, timeout=10000)
    client.client.use(gdpr_auth_middleware)
    return client