# -*- coding: utf-8 -*-
# @Time : 2022/1/26 2:28 下午
# @Author : zhuzhenzhong
import bytedredis


class RedisClient:
    """
    包装bytedredis，具体用法参考https://python.byted.org/library/redis.html
    """
    def __init__(self, psm):
        self.psm = psm
        self._client = None

    @property
    def client(self):
        if self._client is None:
            self._client = bytedredis.Client(redis_psm=self.psm)
        return self._client

    def __getattr__(self, item):
        return getattr(self.client, item)


redis_ad_star = RedisClient(psm='toutiao.redis.ad_star')
#toutiao.redis.ad_star_dev   toutiao.redis.ad_star

if __name__ == '__main__':
    #print(redis_ad_star.set('hello', 'star auto test'))
    print(redis_ad_star.get('STAR|STAR_ADVERTISER_VALIDATE_PHONE|1639752636991496').decode())
    #print(redis_ad_star.delete('hello'))