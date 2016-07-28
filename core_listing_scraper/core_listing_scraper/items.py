# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CraigslistItem(scrapy.Item):
    craig_id = scrapy.Field()
    title = scrapy.Field()
    last_modified_at = scrapy.Field()
    price = scrapy.Field()
    absolute_url = scrapy.Field()
