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


class BrainItem(scrapy.Item):
    name = scrapy.Field()
    path = scrapy.Field()
    url = scrapy.Field()
    description = scrapy.Field()
    group_id = scrapy.Field()


class GoogleItem(scrapy.Item):
    name = scrapy.Field()
    path = scrapy.Field()
    url = scrapy.Field()
    description = scrapy.Field()
    group_id = scrapy.Field()
    app_front_img_url = scrapy.Field()
    game_imgs_urls = scrapy.Field()