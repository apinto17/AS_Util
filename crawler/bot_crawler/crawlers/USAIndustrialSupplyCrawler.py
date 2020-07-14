from bot_crawler import Site as st
import json
import time
from bs4 import BeautifulSoup
import requests


class USAIndustrialSupplyCrawler(st.Site):

    # return terms of service else None
    def terms_of_service(self):
        return None

    # return robots.txt else None
    def robots_txt(self):
        return None

    # return a list of categories as a list of soup objects
    def get_cats(self):
        if self.url == "https://www.usaindustrialsupply.com/index.php":
            return self.browser.find_elements_by_css_selector(
                "ul[class='dropdown dropdown-vertical'] > li > a"
            )
        else:
            subs = self.browser.find_elements_by_css_selector(
                "div.subcategories > ul > li > a"
            )
            return subs

    # param browser object of a category tag
    # return the name of the category as a string
    def get_cat_name(self, cat):
        return cat.text

    # param browser object of the page
    # return the link to the show all page as a string if it exits
    # else return None
    def get_show_all_page(self):
        pass

    # param browser object of the page
    # return a list of pages of products as browser objects
    # else return None
    def get_prod_pages(self):
        pages = self.browser.find_elements_by_css_selector("div.pagination > a")
        return pages
    
    # param browser object of the page
    # return the next page of products as a browser object
    # else return None
    def get_next_page(self):
        pass

    # param browser object of the page
    # return a list of products as browser objects
    def get_prods(self):
        subs = self.browser.find_elements_by_css_selector(
            "div.subcategories > ul > li > a"
        )
        if len(subs) == 0:
            prods = self.browser.find_elements_by_css_selector("div.product-container")
            return prods

    # param browser object of the item to be scraped
    # return item description as a string
    def get_item_desc(self, item):
        desc = item.find_element_by_css_selector("div.product-info > a").text
        return desc

    # param browser object of the item to be scraped
    # return item link as a string
    def get_item_link(self, item):
        link = item.find_element_by_css_selector("div.product-info > a").get_attribute("href")
        return link

    # param browser object of the item to be scraped
    # return item image as a string
    def get_item_image(self, item):
        image = None
        try:
            image = item.find_element_by_css_selector("div.product-item-image > span > a > img").get_attribute("src")
        except:
            pass
        return image

    # param browser object of the item to be scraped
    # return item price as a string
    def get_item_price(self, item):
        price = "".join([p.text for p in item.find_elements_by_css_selector("div.product-info > div.prod-info > div.prices-container > div.product-prices > span > span > span.price")])
        return price

    # param browser object of the item to be scraped
    # return unit that the item is sold in as string ("box of 10")
    def get_item_unit(self, item):
        return ""

    # param browser object of the item being scrapped
    # return all the specs of the item are returned as a string with the format {'key' : 'val'}
    def get_item_specs(self, item=None):
        res = {}
        try:
            spec_rows = self.browser.find_elements_by_css_selector("table > tbody > tr")
            
            for spec in spec_rows:
                children = spec.find_elements_by_xpath("./*")
                if len(children) == 2:
                    text = children[0].text.strip(":").strip()
                    value = children[-1].text.strip()
                    if text != "" and value != "":
                        res[text] = value

        except Exception as e:
            pass
        
        return json.dumps(res)
