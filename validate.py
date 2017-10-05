# -*- coding: utf-8 -*-
import requests
import db

import config


class Vali():
    def __init__(self):
        self.db = db.RedisClient()


    def vali_http_ip(self, ip):
        try:
            requests.get(config.TEST_URL['http'], proxies={'http': 'http://%s' % (ip)},timeout=30)
        except:
            print '%s:failed' % ip
        else:
            if self.db.count('http') < config.IP_MAX:
                self.db.add(ip,'http')
            print '%s:success' % ip

    def vali_https_ip(self, ip):
        try:
            requests.get(config.TEST_URL['https'], proxies={'https': 'https://%s' % (ip)},timeout=30)
        except:
            print '%s:failed' % ip
        else:
            if self.db.count('https') < config.IP_MAX:
                self.db.add(ip,'https')
            print '%s:success' % ip