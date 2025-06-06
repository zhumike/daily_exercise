# coding=utf-8
import requests
import sys
import codecs
import random
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

# host = "http://aweme.snssdk.com.boe-gateway.byted.org"
# path = "/aweme/v1/commerce/star/cps/poi/tag/"
# headers = {"X-TT-ENV": "boe_grouponcenter_zhutest", "Cookie": "sessionid=9394c52a74b673cd8a2b10f9eabc475e;"}
# r = requests.request("GET", url=host + path, headers=headers)
# response = r.json()
# print(response)
# print(sys.getdefaultencoding())
# print(sys.path)

# print(random.sample('zyxwvutsrqponmlkjihgfedcba',5))



# import time
#
# print ("time.time(): %d " %  int(time.time()))
for i in range(3):
    print(i)