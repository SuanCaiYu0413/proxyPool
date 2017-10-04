# -*- coding: utf-8 -*-
import db

r = db.RedisClient()
r.add("123")
r.add("asd")
r.add("grf")
r.add("utyu")
r.add("grf")
print r.count()


# import redis
# r = redis.Redis(host='119.29.194.163', port=6379,db=0)
# r.set('name', 'zhangsan')   #添加
# print (r.get('name'))   #获取