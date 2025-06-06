from random import random

# l1 = ['GetCreatorMissionList', 'GetStarUserStatusDetail', 'GetBaseOcUserInfoByStarId', 'GetStarAuthorTask', 'GetLiveTask', 'GetOrderIdByRoomId', 'GetUserInvalidVideoCnt', 'GetEnterpriseComponentStatus', 'MultiGetSmallAppItemDetail', 'CalculateOrderPrice', 'GetMissionTaskCnt', 'GetUdeskToken', 'GetMissionIndustryBanner', 'GetAuthorOrderAmount', 'GetAuthorStarOrderStatDaily', 'DemanderGetOcUidAndCheckIsRegister', 'GetStarCustomerServiceLink', 'GetChallengeItemStaticInfo', 'MGetStarAuthorId', 'GetTaskItemSettlementInfo', 'GetSmallAppLiveChallengeDetail', 'GetCreatorCenterShowList', 'DemanderGetUniversalOrderSummary', 'CanAuthorRegister', 'SyncDrawUsers', 'GetAssignedTaskList', 'AwemeProfileShouldShowStarCard', 'GetSmallAppItemDailyDetail', 'GetHomeInvalidVideoList', 'MakeCellDecision', 'MultiGetMissionInfo', 'GenerateQrCode', 'DemanderGetUniversalDemandList', 'GetOrderInfoByOrderId', 'GetLiveResourceUrl', 'MGetDouPlusDownloadComponentInfo', 'CreateOrModifyCommonComponent', 'GetAwemeOrderBasicInfo', 'GetStarHotListTag', 'GetActiveLiveTask', 'GetDemanderTradeRecordList', 'GetStarUserInfosByAwemeId', 'MultiGetItemLinkInfo', 'GetDouPlusDownloadComponentInfo', 'GetRoomByTag', 'GetSmallAppChallengeDetail', 'GetStarAuditProcess', 'GetTotalUnreadNum', 'GetMissionPlatformList', 'SyncTaskAuditInfo', 'GetStarMission', 'GetStarDataByPlatformUid', 'GetOrderItem', 'GetAuthorIdByCoreUserId', 'MultiGetItemTaskInfo', 'SearchStarItemInfo', 'MGetStarAuthorInfosForYuntu', 'GetStarItemInfo', 'CalculateChallengeAmount', 'GetSmallAppAuthorInfo', 'MultiCheckStarAuthor', 'GetAwemeActiveOrders', 'CreateStarDemand', 'GetAuthorBusinessAmount', 'MultiGetLiveOrderInfo', 'GetBizLineCouponActivity', 'MultiGetStarEcomPromotion', 'MGetAuthorPrice', 'CreateDemanderCharge', 'GetOrderDemanderInfo', 'GetTaskInfo', 'GetAwemeMissionActiveOrders', 'GetAuthorRecommendPrice', 'GetDouPlusAuditQueueCondition', 'GetStarIdByPlatform', 'GetAwemeUidByStarId', 'GetAuthorIncomeModule', 'GetUdeskSignature', 'SetDemanderCSRTag', 'AwemeGetCorpStarCardInfo', 'OpenStarAuthorTask', 'AwemeLiveStarAuthorTask', 'GetHomeValidVideoList', 'CreateBudgetPlan', 'GetStarAuthorLiveOrderPackageName', 'GetEncourageAuthorInfo', 'CanOneOffWithdraw', 'GetStarAuthorTaskStatus', 'SearchStarItemFansAnalysis', 'CreateDemanderContract']


# l1 = list(filter(lambda x:x,l1))
#
# l1 = list(set(l1))
# print(len(l1))
# print(l1)
#
# c=[n for n in l1 if l1.count(n) > 1]
# print(c)
# import random
# num = random.randint(00000000, 99999999)
# end_num = str(num).zfill(8)
# print(end_num)
#
# t1 = ["sre","apple","ban"]
# t2 = ["ban","sre","apple"]
# t3 = ["sre","apple","ban"]
#
# assert t1 == t3
#
# l1 = [
#         {
#             "code": "CMB",
#             "name": "招商银行"
#         },
#         {
#             "code": "X13064",
#             "name": "山东招远农村商业银行"
#         },
#         {
#             "code": "CMB_YL",
#             "name": "招商永隆银行"
#         }
#     ]
#
# for mem in l1:
#     print(mem)
#
# for i in range(len(l1)):
#     print(l1[i]['name'])


import re

text = "Hello, World! This is a test A."
text2 = "op"
pattern = "[Aa]"

matches = re.findall(pattern, text)

matches2 = re.findall(pattern, text2)




print(matches)  # 将输出所有匹配的'A'或'a'字符的列表
print(matches2)