import thriftpy2
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from lib import rpc
from lib.db import qa_tables

cur_dir = os.path.dirname(os.path.abspath(__file__))
service_ptn = re.compile(r'^\s*service\s+(?P<name>\w+)\s+\{')
inner_services = ['orders','demander','challenge','author','settlement','marketing','mcn','touch','generic','go_demander','go_author','control','go_orders','audit_gateway','task']
outer_services = ['platform','goplatform','saturn']

"""不纳入统计的接口，不会算在接口总数中"""

skip_interfaces = {

    'orders': ['DemanderGetMaterialTemplateDetail','AuthorGetCMaterialOrderList','AuthorGetCMaterialOrderDetail','AdminDeleteMaterialTemplateWhitelist','AuthorGetMaterialOrderStat',
               'AdminUpdateMaterialTemplate','AdminUpdateMaterialTemplateWhitelist','AuthorGetMaterialTemplateDetail','GetAwemeMaterialValidTime','AdminDeleteMaterialTemplate',
               'DemanderGetMaterialOrderStat','DemanderDownloadCMaterial','DemanderGetMaterialOrderSetting','AdminGetMaterialTemplateDetail','AuthorOperateCMaterialOrder',
               'AuthorGetMaterialOrderVideoList','DemanderUploadCMaterial','DemanderDownloadCMaterial','DemanderGetMaterialOrderVideoList','DemanderSyncCMaterial',
               'DemanderGetCMaterialSyncInfo','AuthorReportCMaterial','DemanderGetMaterialTemplateList','AdminCreateMaterialTemplate','AdminGetMaterialTemplateWhitelist'],
    'demander':['AdminSyncBrandInfo','RecommendSimilarAuthors','DeleteJiheBriefProductInfo','SaveJiheBriefProductInfo','GetTest','CreativeDemanderAcceptProtocol'],
    'challenge':['McnSearchAuthorsForContractChallenge','McnCanContractSpeciallyChallenge','McnGetChallengeRewardList','McnGetChallengeItemStatistics',
                 'DemanderPublishOrderForRecruitAuthor','CreateChallenge','UpdateChallengeV2',
                 'AuthorGetChallengeMaterialAuthInfo','DemanderGetCoverUser','DemanderUpdateItemStat',
                 'McnGetProfitAmountForContractChallenge','McnInviteAuthorJoinContractChallenge','McnInviteAllSignedAuthorJoinContractChallenge',
                 'AdminUpdateChallenge','AdminSendChallengeReward','ChooseChallengeItemCheck','AdminUpdateDemanderRejectedValue',
                 'CommanderGetLedDetails','CommanderExportLedDetail','AuthorGetCommanderLandingPageInfo','CommanderReleaseChallenge',
                 'AuthorGetSuggestPrice'],
    'mcn':['GetMcnGradePageInfo','AdminDownloadMcnGradeLarkExcel','McnTest'],
    'author':['CreativeChangeMmmBankInfo','AuthorGetCMaterialList','DemanderGetSpuDetail',
              'AdminGetSpuWhitelist','AuthorGetCMaterialTip','AdminUpdateSpuWhitelist',
              'AdminDeleteSpuWhitelist','AuthorSetCMaterialList','AdminDeleteSpu','AdminGetSpuDetail','AuthorGetSpuList',
              'AdminUpdateSpu','AdminCreateSpu','AdminUpdateSpuStatus','AuthorAcceptCMaterialProtocol','AuthorScoreForDemander','AuthorGetCMaterialInfo'],
    'marketing':['CheckActVisible','Get2021Double11ChallengeList','DemanderReceivePlatformActivityCoupon',
                 'ReceiveActCouponStatus','AdminSendCoupon','GetAuthorAct2021Double11Data','AdminStopCoupon','AdminCreateCoupon'],
    'generic':['GetLiveResourceUrl'],
    'goplatform':['GetRecommendSpuByVideoId','GetCouponConfigOptions','GetUserCouponInfo','GetStarIdByCommerceUserId',
                  'AwemeGetMineStarCardInfo','GetMissionPlatformAuthorInfo','GetAuthorizeItemIdsByShopIdToShowProduct',
                  'OpenStarAuthorTask','GetAuthorRecommendPrice','GetStarAuthorTask','SetStarAuthorTask',
                  'CheckStarAuthorTaskStatus','GetUserMissionSearchTags','CalculateOrderPrice','GetUdeskUserInfo',
                  'GetStarLoginInfo','GetStarInfoByVerifyCode'],
    'platform':['GetCreatorTypes','GetSpuListForEnterprise','GetCallBoe','UpdateBoeCall','MgetBoeCall','CreateCallBoe'],
    'task':['DemanderGetMobileCreativeOrderList','DemanderGetMobileCreativeOrderListV2','AdminQuerySeriesTasks','DemanderGetTaskDemandDetail','AuthorGetTaskDemandDetail','DemanderGetUniversalCampaignList',
            'DemanderGetUniversalCampaignSummary','GetAppTaskDetail','CheckCampaignSyncStatus','DemanderGetCampaignOrderSummary','AuthorGetCampaignOrderSummary','McnGetCampaignOrderSummary',
            'AuthorGetCampaignDemandInfo','DemanderGetCampaignDemandInfo','McnGetCampaignDemandInfo','AuthorGetAvailableChallenges',
            'GetSuggestSearch','GetSuggestSearchByKeyword','GetChildDemanderUniversalTaskList','GetChildDemanderUniversalOrderSummary',
            'GetAuthorMissionSummary'],
    'community':['GetGrouponPermissionLog'],
    'go_author': ['CheckPlanAuthor', 'AuthorGetPlanData', 'AuthorGetPlanLarkPhone', 'AuthorUpdatePlanLarkPhone',
                  'AuthorAbandonPlanSign', 'AuthorGetTargetNotify', 'AuthorConfirmTargetNotify','GetManagerRecommendAuthor','AdminGetCreativeCenterAuthorInfos',
                  'AdminGetCommanderList','AdminCreateCommander','AdminDeleteCommander','CheckAuthorIsCommander','AdminChangePreferAuthorStockStatus'
                  'AdminUpdatePreferAuthorFeeRate','SwitchAuthorManageRecommendDemander','GetAuthorManageRecommendDemander','AuthorSendManageCoupon',
                  'AuthorApplySettlementCard'],
    'go_orders':['GetEcomProjectList','GetEcomBudgetList','DemanderModifyProjectRelation'],
    'go_demander':['GetOneClickCustomerInfo','GetDemanderAwemeInfoByStarId','GetShopList','GetProductList',
                   'SyncDrawUsers','GetBrandModulePermissions','DemanderSearchForProjectAuthors','GetSubscribeStatus']
}


def main():
    methods = get_total_interface()
    for service, info in methods.items():
        rows = qa_tables.interface_info.query_eq(service=info['service_name'])
        tmp = []
        for row in rows:
            if row.method not in skip_interfaces.get(service, []):
                tmp.append(row.method)
        info['methods']['implemented'] = tmp
    for service, info in methods.items():
        print(f'{service} total:{len(info["methods"]["total"])}')
        #print("接口覆盖率数据:%f" % (len(info["methods"]["implemented"]) / len(info["methods"]["total"])))
        not_implemented = list(set(info['methods']['total']) - set(info['methods']['implemented']))
        print("接口覆盖率数据:%f" % ((len(info["methods"]["total"])-len(not_implemented)) / len(info["methods"]["total"])))
        print('interface not implemented:')
        print("共有{}个接口未覆盖".format(len(not_implemented)))
        pprint_list(not_implemented)
        print("共有{}个接口已覆盖 \n".format(len(info["methods"]["total"])-len(not_implemented)))
    print(f'total, total:{sum([len(info["methods"]["total"]) for _, info in methods.items()])}, '
          f'implemented:{sum([len(info["methods"]["implemented"]) for _, info in methods.items()])}')


def pprint_list(array, line_max=120):
    cur_length = 0
    for each in array:
        s = f'"{each}", '
        print(s, end='')
        cur_length += len(s)
        if cur_length >= line_max:
            cur_length = 0
            print()
    print()


def get_total_interface():
    methods = {}
    for service in inner_services:
        rpc.update_idl(f'https://code.byted.org/ad/star_thrift_gen/blob/master/idl/{service}.thrift')
        idl_path = os.path.join(cur_dir, '..', 'ad', 'star_thrift_gen', 'idl', f'{service}.thrift')
        methods[service] = parse(service, idl_path)
    for service in outer_services:
        rpc.update_idl(f'https://code.byted.org/cpputil/service_rpc_idl/blob/master/ad/star/{service}.thrift')
        target = os.path.join(cur_dir, '..', 'cpputil', 'service_rpc_idl', 'toutiao_pgc_core_article.thrift')
        src = os.path.join(cur_dir, '..', 'idl', 'cpputil', 'service_rpc_idl', 'toutiao_pgc_core_article.thrift')
        # https://code.byted.org/cpputil/service_rpc_idl/blob/master/toutiao_pgc_core_article.thrift
        # 这个idl下载有问题，所以本地存放一份，下载到这个idl的时候使用本地副本替换
        shutil.rmtree(target, ignore_errors=True)
        shutil.copy(src, target)
        idl_path = os.path.join(cur_dir, '..', 'cpputil', 'service_rpc_idl', 'ad', 'star', f'{service}.thrift')
        methods[service] = parse(service, idl_path)
    return methods


def parse(service, idl_path):
    with open(idl_path) as fd:
        lines = fd.readlines()
    for i in range(len(lines) - 1, -1, -1):
        line = lines[i]
        tmp = service_ptn.match(line)
        if tmp:
            service_name = tmp.group('name')
            break
    mod = thriftpy2.load(idl_path)
    attrs = dir(mod)
    service_o = None
    for attr in attrs:
        if attr == service_name:
            service_o = getattr(mod, attr)
            break
    return {
        'service_name': service_name,
        'methods': {
            'total': [method for method in service_o.thrift_services if
                      not method.startswith('Inner') and method not in skip_interfaces.get(service, [])]
        }
    }


if __name__ == '__main__':
    exit(main())