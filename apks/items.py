# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ApksItem(scrapy.Item):
    name = scrapy.Field()
    click_url = scrapy.Field()
    json_url = scrapy.Field()
    download_url = scrapy.Field()
