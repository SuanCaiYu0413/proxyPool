# -*- coding: utf-8 -*-
import bs4
import config
import requests
import validate
import threadpool
class XCSpider():


    def __init__(self):
        self.header = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3218.0 Safari/537.36'
        }
        self.pool = threadpool.ThreadPool(15)



    def parser(self):

        http_ip = []
        html = self.read_html('http')
        select = bs4.BeautifulSoup(html, 'lxml')
        trs = select.find_all('table', {'id': 'ip_list'})[0].find_all('tr', {'class': 'odd'})
        for tr in trs:
            tds = tr.find_all('td')
            http_ip.append('%s:%s'%(tds[1].get_text(),tds[2].get_text()))
        request = threadpool.makeRequests(validate.Vali().vali_http_ip, http_ip)
        [self.pool.putRequest(req) for req in request]
        self.pool.wait()

        https_ip = []
        html = self.read_html('https')
        select = bs4.BeautifulSoup(html, 'lxml')
        trs = select.find_all('table', {'id': 'ip_list'})[0].find_all('tr', {'class': 'odd'})
        for tr in trs:
            tds = tr.find_all('td')
            https_ip.append('%s:%s'%(tds[1].get_text(),tds[2].get_text()))
        request = threadpool.makeRequests(validate.Vali().vali_https_ip, https_ip)
        [self.pool.putRequest(req) for req in request]
        self.pool.wait()


    def read_html(self,key):
        req = requests.get(config.IP_URL[key],headers=self.header)
        if req.status_code == 200:
            return req.content
        else:
            return  self.read_html(key)

if __name__ == "__main__":
    a = XCSpider()
    a.parser()