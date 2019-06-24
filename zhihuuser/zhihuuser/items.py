# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihuuserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name=scrapy.Field()
    headline = scrapy.Field()
    url = scrapy.Field()
    avatar_url = scrapy.Field()
    url_token = scrapy.Field()
