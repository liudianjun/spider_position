# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhilianItem(scrapy.Item):

    updateDate = scrapy.Field()
    city = scrapy.Field()
    positionURL = scrapy.Field()
    welfare = scrapy.Field()
    salary = scrapy.Field()
    businessArea = scrapy.Field()
    company = scrapy.Field()
    workingExp = scrapy.Field()
    describtion = scrapy.Field()
    job_title = scrapy.Field()


class LaGouItem(scrapy.Item):

    positionId = scrapy.Field()
    updateDate = scrapy.Field()
    city = scrapy.Field()
    # positionURL = scrapy.Field()
    welfare = scrapy.Field()
    salary = scrapy.Field()
    businessArea = scrapy.Field()
    company = scrapy.Field()
    workingExp = scrapy.Field()
    describtion = scrapy.Field()
    job_title = scrapy.Field()

class job51Item(scrapy.Item):
    job_title = scrapy.Field()
    updateDate = scrapy.Field()
    city = scrapy.Field()
    welfare = scrapy.Field()
    salary = scrapy.Field()
    # businessArea = scrapy.Field()
    company = scrapy.Field()
    workingExp = scrapy.Field()
    describtion = scrapy.Field()
