# -*- coding: utf-8 -*-
import scrapy
from .bhid_site import Bhid
from items_crawler.items import Item
from scrapy_splash import SplashRequest
import random
from scrapy.shell import inspect_response



class BhidCrawlerSpider(scrapy.Spider):
    name = 'bhid_crawler'
    allowed_domains = ['www.bhid.com']
    start_urls = ['https://www.bhid.com/']

    def __init__(self):
        self.site = Bhid('https://www.bhid.com/', "bhid.com", 'https://www.bhid.com/')

    # TODO maybe instead of setting up proxies in middlewares, you could just add them in the SplashRequest?
    def start_requests(self):
        yield SplashRequest(
            url="https://www.bhid.com//CatSearch/1189/pipe-layout-markers",
            callback=self.parse,
        )

    def parse(self,response):
        if(self.site.is_cat_page(response)):
            for cat in self.site.get_cats(response):
                url = self.site.get_cat_link(cat, response)
                old_cats = self.site.cats
                self.site.cats += "|" + self.site.get_cat_name(cat, response)
                yield SplashRequest(url, callback=self.parse)
                self.site.cats = old_cats

        elif(self.site.is_prod_page(response)):
            #TODO implement functionality to flip through pages
            #TODO log every time you cant scrape an item and put try except around it
            for prod in self.site.get_prods(response):
                yield self.parse_prod(prod)

    
    def parse_prod(self, prod):
        item = Item()

        desc = self.site.get_item_desc(prod)
        link = self.site.get_item_link(prod)
        img = self.site.get_item_image(prod)
        price = self.site.get_item_price(prod)
        unit = self.site.get_item_unit(prod)
        sitename = "bhid.com"
        specs = "In testing"

        #Put each element into its item attribute.
        item['desc'] = desc
        item['link'] = link
        try:
            item['img'] = img
        except:
            pass
        item['price'] = price
        try:
            item['unit'] = unit
        except:
            pass
        item['sitename'] = sitename
        try:
            item['specs'] = specs
        except:
            pass

        self.logger.info(item['desc'])

        return item


 