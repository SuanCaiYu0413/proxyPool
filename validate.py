# -*- coding: utf-8 -*-
import requests
import threadpool

import db

import config


class Vali():
    def __init__(self):
        self.db = db.RedisClient()


    def vali_http_ip(self, ip):
        try:
            requests.get(config.TEST_URL['http'], proxies={'http': 'http://%s' % (ip)})
        except:
            print '%s:failed' % ip
        else:
            self.db.add(ip,'http')
            print '%s:success' % ip

    def vali_https_ip(self, ip):
        try:
            requests.get(config.TEST_URL['https'], proxies={'https': 'https://%s' % (ip)})
        except:
            print '%s:failed' % ip
        else:
            self.db.add(ip,'https')
            print '%s:success' % ip


    def vali_all(self):
        self.pool = threadpool.ThreadPool(15)
        http_count = self.db.count('http')
        http_ips = []
        https_ips = []
        https_count = self.db.count('https')
        for i in range(http_count):
            http_ips.append( self.db.get('http'))
        for i in range(https_count):
            https_ips.append( self.db.get('https'))

        request = threadpool.makeRequests(self.vali_http_ip, http_ips)
        [self.pool.putRequest(req) for req in request]
        self.pool.wait()

        request = threadpool.makeRequests(self.vali_https_ip, https_ips)
        [self.pool.putRequest(req) for req in request]
        self.pool.wait()