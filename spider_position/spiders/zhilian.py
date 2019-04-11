# -*- coding: utf-8 -*-
import scrapy
from spider_position.items import ZhilianItem
import json
from math import ceil
from copy import deepcopy


class ZhilianSpider(scrapy.Spider):
    # start 设置请求的位置
    # pageSize 设置每次请求数据的数量
    base_url = 'https://fe-api.zhaopin.com/c/i/sou?start=0&pageSize=30&cityId=530&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw=%E7%88%AC%E8%99%AB&kt=3&_v=0.62418367&x-zp-page-request-id=17f6e9fe2b3a4776b76c92e927e0b00c-1554707343327-86943'
    req_url = 'https://fe-api.zhaopin.com/c/i/sou?start={}&pageSize=30&cityId=530&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw=%E7%88%AC%E8%99%AB&kt=3&_v=0.62418367&x-zp-page-request-id=17f6e9fe2b3a4776b76c92e927e0b00c-1554707343327-86943'
    name = 'zhilian'
    allowed_domains = ['zhaopin.com']
    start_urls = [base_url]

    def parse(self, response):
        item = ZhilianItem()
        data = response.text
        json_data = json.loads(data)
        results = json_data['data']['results']

        for result in results:
            item['updateDate'] = result['updateDate']
            item['city'] = result['city']['display']
            item['positionURL'] = result['positionURL']
            item['welfare'] = ''.join(result['welfare'])
            item['salary'] = result['salary']
            try:
                item['businessArea'] = result['businessArea']
            except:
                item['businessArea'] = None
            item['company'] = result['company']['name']
            item['workingExp'] = result['workingExp']['name']
            # print(item)
            yield scrapy.Request(item['positionURL'], callback=self.parse_content,
                                 meta={'item':deepcopy(item)})

        numFound = json_data['data']['numFound']
        print(numFound)
        for i in range(1, ceil(numFound / 30) + 1):
            yield scrapy.Request(self.req_url.format(i * 30), callback=self.parse)


    def parse_content(self, response):
        item = response.meta['item']
        describtion = response.xpath("//div[@class='describtion__detail-content']//text()").extract()
        job_title = ''.join(response.xpath("//h3[@class='summary-plane__title']/text()").extract())
        # print(''.join(describtion).strip())
        item['describtion'] = ''.join(describtion).strip()
        item['job_title'] = job_title

        # print(job_title)
        return item
