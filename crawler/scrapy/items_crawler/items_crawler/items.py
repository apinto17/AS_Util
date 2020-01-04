# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ItemsCrawlerItem(scrapy.Item):
    desc = scrapy.Field
    link = scrapy.Field
    img = scrapy.Field
    price = scrapy.Field
    unit = scrapy.Field
    sitename = scrapy.Field
    specs = scrapy.Field
