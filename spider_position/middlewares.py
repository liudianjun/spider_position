# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
from scrapy import signals
import random
from scrapy.http.headers import Headers
from spider_position.get_cookie import GetCookie
import random
import base64
import requests
import json
from spider_position.proxymodel import ProxyModel
from twisted.internet.defer import DeferredLock


class Randon_headers(object):

    def __init__(self):
        self.user_agent = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
        'Opera/8.0 (Windows NT 5.1; U; en)',
        'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER) ',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)"',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11',
        ]
        self.cookies = ()


    def process_request(self, request, spider):
        """
        设置随机请求头，拉勾网有特殊的反扒手段，需要完整的请求头和cookie信息， 而且cookie
        有效时间比较短
        :param request:
        :param spider:
        :return:
        """
        ua = random.choice(self.user_agent)
        request_headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        # 'Content-Length': '37', # 添加这个参数请求不到数据
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'www.lagou.com',
        'Origin': 'https://www.lagou.com',
        'Referer': 'https://www.lagou.com/jobs/list_%E7%88%AC%E8%99%AB?city=%E5%8C%97%E4%BA%AC&cl=false&fromSearch=true&labelWords=&suginput=',
        'X-Anit-Forge-Code': '0',
        'X-Anit-Forge-Token': 'None',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }


        if spider.name == 'lagou':
            # 拉钩爬虫做特殊的处理
            if len(self.cookies) == 0:
                url = 'https://www.lagou.com/jobs/list_?city=%E5%8C%97%E4%BA%AC&cl=false&fromSearch=true&labelWords=&suginput='
                self.cookies = GetCookie(url=url).get_cookies
            request.headers = Headers(request_headers)
            request.headers['User-Agent'] = ua
            request.cookies = self.cookies
        # print(ua)
        request.headers['User-Agent'] = ua
        # return None

    def process_response(self, request, response, spider):

        # print('操作频繁', response.text)
        if response.status == 302:
        # if '您操作太频繁' in response.text or '页面加载中' in response.text:
            self.cookies = ()
            print('*'*50)
            print('更新cookie')
            print('*'*50)
            return request

        return response


class IPDowmloadMinddleware(object):

    PROXY_URL = 'http://http.tiqu.alicdns.com/getip3?num=1&type=2&pro=&city=0&yys=0&port=11&time=1&ts=1&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions='

    def __init__(self):
        super(IPDowmloadMinddleware, self).__init__()
        # 获取代理属性
        self.current_proxy = None
        self.lock = DeferredLock()

    def process_request(self, request, spider):
        if spider.name == 'lagou':
            # 如果没设置代理 或者代理即将过期 更新代理
            if 'proxy' not in request.meta or self.current_proxy.is_expiring:
                self.update_proxy()
            request.meta['proxy'] = self.current_proxy.proxy

        # print("请求代理", self.current_proxy.proxy)
        # request.meta['proxy'] = 'https://58.218.92.116:5803'
        # print(request.meta)

    def process_response(self, request, response, spider):
        if spider.name == 'lagou':
        # 如果请求没有成功 或者跳转到验证码页面 更新代理ip
            print('==response.status==', response.status)
            if '您操作太频繁' in response.text or '页面加载中' in response.text:

                print('====>>>', response.url)
                if not self.current_proxy.is_blacked:
                    self.current_proxy.is_blacked = True
                self.update_proxy()
                # 返回request 让这次请求从新回到调度中 再次请求
                return request
        # 返回响应，如果不反回就得不到解析
        return response

    def update_proxy(self):
        # 因为twisted是异步执行的 所有需要加锁
        self.lock.acquire()
        # 判断获取ip的条件，如果是第一次 或者即将过期
        if not self.current_proxy or self.current_proxy.is_expiring or self.current_proxy.is_blacked:
            # 请求IP
            response = requests.get(self.PROXY_URL)
            result = json.loads(response.text)

            print('--' * 50)
            print(result)
            # 获取Ip
            # 芝麻代理获取IP的链接如果访问频率太高就会有警示
            if len(result['data']) > 0:
                data = result['data'][0]
                proxy_model = ProxyModel(data)
                self.current_proxy = proxy_model
                # print(self.current_proxy.is_expiring, self.current_proxy.is_blacked)
                print('--' * 50)
        # 获取ip后解锁
        self.lock.release()


