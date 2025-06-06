# -*- coding: utf-8 -*-
# @Time : 2022/10/14 10:45 上午
# @Author : zhuzhenzhong
demander_id=1639752636991496
REDIS_SYS_PREFIX = 'STAR'
AdvertiserValidatePhoneNumberRedisPrefix = REDIS_SYS_PREFIX + '|STAR_ADVERTISER_VALIDATE_PHONE|'
redis_key = AdvertiserValidatePhoneNumberRedisPrefix + str(demander_id)
print(redis_key)
print(type(redis_key))

