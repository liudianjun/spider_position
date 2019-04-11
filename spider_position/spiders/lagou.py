# -*- coding: utf-8 -*-
import scrapy
import time
import json
from spider_position.items import LaGouItem
import math
from copy import deepcopy


class LagouSpider(scrapy.Spider):

    f = 0
    name = 'lagou'
    allowed_domains = ['lagou.com']
    start_urls = ['https://www.lagou.com/jobs/positionAjax.json?city=%E5%8C%97%E4%BA%AC&needAddtionalResult=false']
    start_url = 'https://www.lagou.com/jobs/positionAjax.json?city=%E5%8C%97%E4%BA%AC&needAddtionalResult=false'
    form_data = {
        'first': 'true',
        'pn': '1',
        'kd': '爬虫'
    }

    def start_requests(self):
        print('------start------')
        yield scrapy.FormRequest(url=self.start_url, formdata=dict(self.form_data), callback=self.parse)

    def parse(self, response):
        print('---------parse-----------')
        lagouitem = LaGouItem()
        # print(response.text)
        json_response = json.loads(response.text)
        totalCount = json_response['content']['positionResult']['totalCount']
        results = json_response['content']['positionResult']['result']
        # print(results)
        for result in results:
            lagouitem['positionId'] = result['positionId']
            lagouitem['company'] = result['companyFullName']
            lagouitem['updateDate'] = result['createTime']
            lagouitem['city'] = result['district']
            lagouitem['welfare'] = result['positionAdvantage']
            lagouitem['salary'] = result['salary']
            lagouitem['businessArea'] = result['businessZones']
            if isinstance(lagouitem['businessArea'], list):
                lagouitem['businessArea'] = ''.join(lagouitem['businessArea']).strip()
            lagouitem['workingExp'] = result['workYear']
            lagouitem['job_title'] = result['positionName']
            content_url = 'https://www.lagou.com/jobs/{}.html'
            yield scrapy.Request(content_url.format(lagouitem['positionId']),
                                 callback=self.parse_content,
                                 meta={'item': deepcopy(lagouitem), 'handle_httpstatus_list': [302]},
                                 dont_filter=True
                                 )


        for i in range(2, math.ceil(totalCount / 15) + 1):
            # if i <= math.ceil(totalCount / 15) + 1:
            form_data = {
                'first': 'false',
                'pn': str(i),
                'kd': '爬虫'
            }
            # print(form_data)
            # print('----当前第{}页'.format(i))
            yield scrapy.FormRequest(url=self.start_url, formdata=form_data, callback=self.parse)


    def parse_content(self, response):

        lagouitem = response.meta['item']
        lagouitem['describtion'] = response.xpath("//*[@id='job_detail']//dd[@class='job_bt']//text()").extract()

        print(self.f)
        self.f += 1
        #
        lagouitem['describtion'] = ''.join(lagouitem['describtion']).strip()
        print(lagouitem['describtion'])
        # print(lagouitem)
        yield lagouitem

