
# -*- coding: utf-8 -*-
import scrapy
from .kele_site import Kele
from items_crawler.items import Item
from scrapy_splash import SplashRequest
import random
from scrapy.shell import inspect_response
import json


class KeleCrawlerSpider(scrapy.Spider):
    name = 'kele_crawler'
    allowed_domains = ['www.kele.com']
    start_urls = ['http://www.kele.com/']
    http_user = 'user'
    http_pass = 'userpass'

    def __init__(self):
        self.site = Kele('https://www.kele.com/product-categories.aspx', "kele.com", 'https://www.kele.com/')
        self.proxy_pool = ['http://astest:assembledtesting123@154.16.91.138:12345',
                            'http://astest:assembledtesting123@154.16.91.196:12345',
                            'http://astest:assembledtesting123@179.61.155.204:12345',
                            'http://astest:assembledtesting123@107.172.130.72:12345',
                            'http://astest:assembledtesting123@198.23.238.96:12345']

    def get_request(self, url, callback, cb_kwargs=None):
        script = """
            function main(splash)
            splash.private_mode_enabled = false
            local url = splash.args.url
            assert(splash:go(url))
            assert(splash:wait(1))
            return {
                html = splash:html(),
                png = splash:png(),
                har = splash:har(),
            }
            end
        """
        if(cb_kwargs is None):
            req = SplashRequest(
                url=url,
                callback=callback,
                endpoint='execute',
                args={'lua_source': script}
            )
        else:
            req = SplashRequest(
                url=url,
                callback=callback,
                endpoint='execute',
                cb_kwargs=cb_kwargs,
                args={'lua_source': script}
            )
        if self.proxy_pool:
            req.meta['splash']['args']['proxy'] = random.choice(self.proxy_pool)
            req.meta['splash']['private_mode_enabled'] = False
        return req
    

    def start_requests(self):
        yield self.get_request(self.site.url, self.parse)
        


    def parse(self,response):
        inspect_response(response, self)
        if(self.site.is_cat_page(response)):
            for cat in self.site.get_cats(response):
                url = self.site.get_cat_link(cat, response)
                yield self.get_request(url, self.parse)

        elif(self.site.is_prod_page(response)):
            count = 1
            for prod in self.site.get_prods(response):
                # try:
                item_dict = self.get_item_data(prod, response)
                yield self.parse_prod(prod, item_dict)
                # except:
                #     self.logger.error("URL: " + response.url + " Could not scrape item number " + str(count))
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
        sitename = "directtools.com"

        return {"desc" : desc, "cats" : cats, "link" : link, "img" : img, "price" : price, "unit" : unit, "sitename" : sitename}


    
    def parse_prod(self, response, item_dict):
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



 