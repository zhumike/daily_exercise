# -*- coding: utf-8 -*-
'''
@Author : zhuzhenzhong
@File : abasetest.py
'''
import bytedabase
client = bytedabase.Client(psm="abase_ad_star", table="author", retry=1, socket_timeout=0.25, socket_connect_timeout=0.3)
key = '[author_star_settlement_card_apply_history]:6885640802911911949'
# client.set(key, "xxxx")
print(client.get(key))
# assert client.ttl(key) == -1
print("test")