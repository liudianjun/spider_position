# -*- coding: utf-8 -*-
import scrapy
from spider_position.items import job51Item
import re
from copy import deepcopy

class Job51Spider(scrapy.Spider):
    name = 'job51'
    allowed_domains = ['51job.com']
    start_urls = ['https://search.51job.com/list/010000,000000,0000,00,9,99,%25E7%2588%25AC%25E8%2599%25AB,2,1.html?']

    def parse(self, response):
        '''
        解析职位列表页面 //*[@id="resultList"]/div[4]/p/span/a
        :param response:
        :return:
        '''
        job51_item = job51Item()
        div_list = response.xpath("//div[@class='el']")
        print(len(div_list))
        for div in div_list:
            job_url = div.xpath("./p[1]//span/a/@href").extract()
            # print(job_url)
            if len(job_url) > 0:
                job51_item['city'] = div.xpath(".//span[@class='t3']/text()").extract_first()
                yield scrapy.Request(url=job_url[0], callback=self.parse_content, meta={'item':deepcopy(job51_item)})


        next_page = response.xpath("//div[@class='p_in']/ul//li/a/@href").extract()[-1]
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)
            # print(next_page)
    def parse_content(self, response):
        # print(response.text)

        job51_item = response.meta['item']
        # 有些页面会不一样，导致部分数据没有，所有要给初始化
        job51_item['updateDate'] = ''
        job51_item['workingExp'] = ''
        job51_item['job_title'] = response.xpath("//div[@class='cn']/h1/@title").extract_first()
        msg = response.xpath("//div[@class='cn']//p[@class='msg ltype']/@title").extract()
        if msg:
            msg = msg[0].split("|")
        for message in msg:
            # print(msg)

            if '发布' in message:
                message = re.findall(r'\d.*\d', message.strip())
                job51_item['updateDate'] = message[0]


            if '经验' in message:
                job51_item['workingExp'] = message.strip()

        job51_item['welfare'] = ','.join(response.xpath("//div[@class='cn']//div[@class='jtag']//span//text()").extract())
        job51_item['salary'] = response.xpath("//div[@class='cn']//strong/text()").extract()
        if job51_item['salary']:
            job51_item['salary'] = job51_item['salary'][0]
        else:
            job51_item['salary'] = '面议'
        # job51_item['businessArea'] = response.xpath("//div[@class='cn']/h1/@title").extract_first()
        job51_item['company'] = response.xpath("//div[@class='cn']//p[@class='cname']/a/@title").extract_first()
        job51_item['describtion'] = re.sub(r'\s', '', ''.join(response.xpath("//div[@class='bmsg job_msg inbox']//text()").extract())).encode('utf-8').decode('utf-8')
        # print(job51_item['city'])
        return job51_item