# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from lagou.mongodbutil import MongodbUtil


class LagouPipeline(object):
    def process_item(self, item, spider):
        if spider.status == 200:
            mongo = MongodbUtil(collection=spider.keyword, db='lagou')
            if mongo.is_exist({'url': item['url']}):
                print("{}已存在".format(item['url']))
            else:
                mongo.insert(item)
                return item
        else:
            mongo = MongodbUtil(collection='error', db='lagou')
            if mongo.is_exist({'url': item['url']}):
                print("{}已存在".format(item['url']))
            else:
                mongo.insert(item)
                return item
