# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pandas as pd
from core_listing_scraper.items import CraigslistItem

DATA_FILE = 'data.csv'

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
        df = pd.DataFrame(self.data)
        df.to_csv(DATA_FILE, index=False)
