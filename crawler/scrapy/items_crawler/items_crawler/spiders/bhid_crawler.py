# -*- coding: utf-8 -*-
import scrapy
from .bhid_site import Bhid
from items_crawler.items import Item
from scrapy_splash import SplashRequest
import random
from scrapy.shell import inspect_response
import json


class BhidCrawlerSpider(scrapy.Spider):
    name = 'bhid_crawler'
    allowed_domains = ['www.bhid.com']
    start_urls = ['https://www.bhid.com/']

    def __init__(self):
        self.site = Bhid('https://www.bhid.com/', "bhid.com", 'https://www.bhid.com/')
        self.proxy_pool = ['http://astest:assembledtesting123@154.16.91.138:12345',
                            'http://astest:assembledtesting123@154.16.91.196:12345',
                            'http://astest:assembledtesting123@179.61.155.204:12345',
                            'http://astest:assembledtesting123@107.172.130.72:12345',
                            'http://astest:assembledtesting123@198.23.238.96:12345']

    def get_request(self, url, callback, cb_kwargs=None):
        if(cb_kwargs is None):
            req = SplashRequest(
                url=url,
                callback=callback,
            )
        else:
            req = SplashRequest(
                url=url,
                callback=callback,
                cb_kwargs=cb_kwargs,
            )
        if self.proxy_pool:
            req.meta['splash']['args']['proxy'] = random.choice(self.proxy_pool)
        return req
    

    def start_requests(self):
        # yield SplashRequest(
        #     url="https://www.bhid.com/",
        #     callback=self.parse,
        # )
        yield self.get_request("https://www.bhid.com/", self.parse)
        


    def parse(self,response):
        if(self.site.is_cat_page(response)):
            for cat in self.site.get_cats(response):
                url = self.site.get_cat_link(cat, response)
                yield self.get_request(url, self.parse)

        elif(self.site.is_prod_page(response)):
            count = 1
            for prod in self.site.get_prods(response):
                try:
                    item_dict = self.get_item_data(prod, response)
                    if(self.site.specs_on_same_page(prod)):
                        yield self.parse_prod(prod, item_dict)
                    else:
                        yield self.get_request(item_dict['link'], self.parse_prod, item_dict)
                except:
                    self.logger.error("URL: " + response.url + " Could not scrape item number " + str(count))
                count += 1
            if(self.site.has_page_turner(response)):
                url = self.site.get_next_page_link(response)
                yield self.get_request(url, self.parse)


    def get_item_data(self, prod, response):
        desc = self.site.get_item_desc(prod)
        cats = self.site.get_cat_string(response)
        link = self.site.get_item_link(prod)
        img = None
        try:
            img = self.site.get_item_image(prod)
        except:
            pass
        price = self.site.get_item_price(prod)
        unit = None
        try:
            unit = self.site.get_item_unit(prod)
        except:
            pass
        sitename = "bhid.com"

        return {"desc" : desc, "cats" : cats, "link" : link, "img" : img, "price" : price, "unit" : unit, "sitename" : sitename}


    
    def parse_prod(self, response, **item_dict):
        item = Item()

        item['desc'] = item_dict["desc"]
        item['cats'] = item_dict["cats"]
        item['link'] = item_dict["link"]
        item['img'] = item_dict["img"]
        item['price'] = item_dict["price"]
        item['unit'] = item_dict["unit"]
        item['sitename'] = item_dict["sitename"]
        try:
            item['specs'] = self.site.get_item_specs(response)
        except:
            item['specs'] = json.dumps({})

        return item



 