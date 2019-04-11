"""
这个模块用来处理请求的proxy数据

"""
from datetime import datetime, timedelta
import requests
import json


class ProxyModel(object):
    def __init__(self, data):
        self.ip = data['ip']
        self.port = data['port']
        self.expire_str = data['expire_time']
        self.proxy = 'https://{}:{}'.format(self.ip, self.port)
        # ip是否被拉黑的标志
        self.is_blacked = False
        print('获取代理---->', self.proxy)
    # 把方法变成属性
    @property
    def expire_time(self):
        """
        获取过期时间
        :return:
        """
        date_time = self.expire_str.split(' ')
        date_str = date_time[0]
        time_str = date_time[1]
        year = int(date_str.split('-')[0])
        month = int(date_str.split('-')[1])
        day = int(date_str.split('-')[2])

        hour = int(time_str.split(':')[0])
        minute = int(time_str.split(':')[1])
        second = int(time_str.split(':')[2])
        # 创建datetime
        date_time = datetime(
            year=year, month=month, day=day,
            hour=hour, minute=minute, second=second
                             )

        return date_time

    @property
    def is_expiring(self):
        """
        判断IP是否即将过期
        :return:
        """
        now = datetime.now()
        if (self.expire_time - now) > timedelta(5):
            return True
        else:
            return False

if __name__ == '__main__':

    url = 'http://http.tiqu.alicdns.com/getip3?num=1&type=2&pro=&city=0&yys=0&port=11&time=1&ts=1&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions='
    resp = requests.get(url)
    result = json.loads(resp.text)
    # 获取Ip
    data = result['data'][0]
    proxy = ProxyModel(data)
    print(proxy.expire_time - datetime.now(), proxy.is_expiring)