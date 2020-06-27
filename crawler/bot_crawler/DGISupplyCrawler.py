import Site as st
import json
import time
from bs4 import BeautifulSoup
import requests


class DGISupplyCrawler(st.Site):

    # return terms of service else None
    def terms_of_service(self):
        return None

    # return robots.txt else None
    def robots_txt(self):
        return None

    # return a list of categories as a list of soup objects
    def get_cats(self):
        cats = self.browser.find_elements_by_css_selector("div.containerRow-contents > div.UDPC > h3 > a")
        if len(cats) == 0:
            cats = self.browser.find_elements_by_css_selector("li.ish-categoryList-item")
        return cats

    # param browser object of a category tag
    # return the name of the category as a string
    def get_cat_name(self, cat):
        cat_name = ""
        try:
            cat_name = cat.find_element_by_css_selector("h4").text
        except:
            cat_name = cat.text
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
        pass
    
    # param browser object of the page
    # return the next page of products as a browser object
    # else return None
    def get_next_page(self):
        next_page_button = self.browser.find_element_by_css_selector("li.ish-pagination-list-next > a").get_attribute("href")
        return next_page_button

    # param browser object of the page
    # return a list of products as browser objects
    def get_prods(self):
        prods = self.browser.find_elements_by_css_selector("div.cms-productTileHorizontal-contents")
        return prods

    # param browser object of the item to be scraped
    # return item description as a string
    def get_item_desc(self, item):
        desc = item.find_element_by_css_selector("div.ish-productTitle").text
        return desc

    # param browser object of the item to be scraped
    # return item link as a string
    def get_item_link(self, item):
        link = item.find_element_by_css_selector("a.kor-product-link").get_attribute("href")
        print("link", link)
        return link
        
    # param browser object of the item to be scraped
    # return item image as a string
    def get_item_image(self, item):
        image = item.find_element_by_css_selector("div.kor-product-photo > img").get_attribute("src")
        print("image", image)
        return image

    # param browser object of the item to be scraped
    # return item price as a string
    def get_item_price(self, item):
        price = item.find_element_by_css_selector("span.kor-product-sale-price-value").text
        print("price", price)
        return price

    # param browser object of the item to be scraped
    # return unit that the item is sold in as string ("box of 10")
    def get_item_unit(self, item):
        return ""

    # param browser object of the item being scrapped
    # return all the specs of the item are returned as a string with the format {'key' : 'val'}
    def get_item_specs(self, item=None):
        res = {}
        if(item is None):
            return json.dumps(res)
        return json.dumps(res)
