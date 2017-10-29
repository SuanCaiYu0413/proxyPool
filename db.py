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

    def get(self,key):
        if self.count(key) < 1:
            return None
        address = self.r.spop('proxy_list_%s'%key)
        return address


    def add(self,value,key):
        return self.r.sadd('proxy_list_%s'%key,value)

    def count(self,key):
        return self.r.scard('proxy_list_%s'%key)