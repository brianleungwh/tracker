# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from core_listing_scraper.items import CraigslistItem

import redis
r = redis.StrictRedis(host='redis', port=6379, db=0)

class CoreListingScraperPipeline(object):

    def __init__(self):
        self.data = []

    def process_item(self, item, spider):
        data = {
            'craig_id': item['craig_id'],
            'title': item['title'],
            'last_modified_at': item['last_modified_at'],
            'price': item['price'],
            'absolute_url': item['absolute_url']
        }
        self.data.append(data)
        return item

    def close_spider(self, spider):
        r.set(spider.results_page_url, json.dumps(self.data, encoding='utf-8'))
