# -*- coding: utf-8 -*-
'''
    建立redis连接池
'''
import redis
import requests
import config
class RedisClient():
    def __init__(self):
        pool = redis.ConnectionPool(host=config.REDIS_HOST,port=config.REDIS_PORT)
        self.r = redis.Redis(connection_pool=pool)

    def get(self):
        if self.count() < 1:
            return None
        address = self.r.spop('proxy_list')
        r = requests.get(config.TEST_URL,proxies=address)
        if r.status_code == '200':
            return address
        else:
            return self.get()

    def add(self,value):
        self.r.sadd('proxy_list',value)

    def count(self):
        return self.r.scard('proxy_list')