# -*- coding: utf-8 -*-
import threading
import proxy_spider
import db
from flask import Flask,jsonify
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello SCY Proxy Pool!'

@app.route('/get/<key>')
def get_ip(key):
    if key == None:
        return jsonify({'ip':'None','key':'None'})
    ip = db.RedisClient().get(key)
    if ip:
        return jsonify({'ip':ip,'key':key})
    else:
        return jsonify({'ip':'None','key':key})

def crawl():
    a = proxy_spider.XCSpider()
    a.parser()
    global timer
    timer = threading.Timer(900, crawl)
    timer.start()


if __name__ == "__main__":
    timer = threading.Timer(1, crawl)
    timer.start()
    app.run(host='0.0.0.0')