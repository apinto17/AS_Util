# -*- coding: utf-8 -*-
import scrapy


class BhidCrawlerSpider(scrapy.Spider):
    name = 'bhid_crawler'
    allowed_domains = ['https://www.bhid.com/']
    start_urls = ['http://https://www.bhid.com//']

    def __init__(self):
        self.declare_css()


    def declare_css(self):


    def parse(self, response):
        pass
