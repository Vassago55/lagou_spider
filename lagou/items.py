# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LagouItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    company = scrapy.Field()
    name = scrapy.Field()
    salary = scrapy.Field()
    address = scrapy.Field()
    experience = scrapy.Field()
    education = scrapy.Field()
    type = scrapy.Field()
    advantage = scrapy.Field()
    description = scrapy.Field()
    evaluate = scrapy.Field()
    label = scrapy.Field()
    location = scrapy.Field()
    code = scrapy.Field()
    keyword = scrapy.Field()
    id = scrapy.Field()
    _id = scrapy.Field()

