# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import JsonLinesItemExporter
import pymysql
from twisted.enterprise import adbapi
from pymysql import cursors


class zhaopinPipeline(object):

    def __init__(self):
        self.f = 0
        self.zhilian_data = open('zhilian.json', 'wb')
        self.lagou_data = open('lagou.json', 'wb')
        self.zhilian_insert = JsonLinesItemExporter(self.zhilian_data, ensure_ascii = False)
        self.lagou_insert = JsonLinesItemExporter(self.lagou_data, ensure_ascii = False)
    def process_item(self, item, spider):
        # print('spider name:', spider.name)
        if spider.name == 'zhilian':
            self.zhilian_insert.export_item(item)

        if spider.name == 'lagou':
            self.lagou_insert.export_item(item)

    def colse_spider(self, spider):
        self.zhilian_data.close()
        self.lagou_data.close()


class Position_mysql_Pipelines(object):
    param = {
        'host': 'localhost',
        'user': 'root',
        'port': 3306,
        'password': 'password',
        'database': 'spider_position',
        'charset': 'utf8',
        'cursorclass': cursors.DictCursor
    }

    def __init__(self):
        # self.f = 0
        self.adbpool = adbapi.ConnectionPool('pymysql', **self.param)
        self._sql = None

    def process_item(self, item, spider):
        if spider.name == 'lagou':
            # 插入数据函数放进异步池
            defer = self.adbpool.runInteraction(self.insert_lagou_item, item)
            # 如果插入数据时候出错会执行addErrback函数
            defer.addErrback(self.handle_error, item)
            # print(self.f)
            # self.f  += 1
        if spider.name == 'job51':
            # 插入数据函数放进异步池
            defer = self.adbpool.runInteraction(self.insert_job51_item, item)
            # 如果插入数据时候出错会执行addErrback函数
            defer.addErrback(self.handle_error, item)

        if spider.name == 'zhilian':
            # 插入数据函数放进异步池
            defer = self.adbpool.runInteraction(self.insert_zhilian_item, item)
            # 如果插入数据时候出错会执行addErrback函数
            defer.addErrback(self.handle_error, item)


    def insert_lagou_item(self, cursor, item):
        # print('--->', item)
        cursor.execute(self.sql_lagou, (
                                   item['positionId'], item['updateDate'], item['city'],
                                   item['welfare'], item['salary'],
                                   item['businessArea'], item['company'], item['workingExp'], item['describtion'], item['job_title'],
                                  ))

    @property
    def sql_lagou(self):
        if not self._sql:
            self._sql = 'insert into position (positionId, updateDate, city, welfare, salary, businessArea, company, workingExp, describtion, job_title) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            return self._sql
        return self._sql


    def insert_job51_item(self, cursor, item):
        # print('--->', item)
        cursor.execute(self.sql_job51, (
                                   item['updateDate'], item['city'],
                                   item['welfare'], item['salary'],
                                   item['company'], item['workingExp'],
                                   item['describtion'], item['job_title'],
                                  ))

    @property
    def sql_job51(self):
        if not self._sql:
            self._sql = 'insert into job51_item (updateDate, city, welfare, salary,  company, workingExp, describtion, job_title) values (%s, %s, %s, %s, %s, %s, %s, %s)'
            return self._sql
        return self._sql


    def insert_zhilian_item(self, cursor, item):
        # print('--->', item)
        cursor.execute(self.sql_zhilian, (
                                   item['updateDate'], item['city'],
                                   item['welfare'], item['salary'],
                                   item['company'], item['workingExp'],
                                   item['describtion'], item['job_title'], item['businessArea']
                                  ))

    @property
    def sql_zhilian(self):
        if not self._sql:
            self._sql = 'insert into zhilian_item (updateDate, city, welfare, salary,  company, workingExp, describtion, job_title, businessArea) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
            return self._sql
        return self._sql


    def handle_error(self, error, item):
        print("写入数据库出错")
        print(error)
        print(item)