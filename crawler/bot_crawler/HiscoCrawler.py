import Site as st
import json
import time
from bs4 import BeautifulSoup


class HiscoCrawler(st.Site):

    # return terms of service else None
    def terms_of_service(self):
        return None

    # return robots.txt else None
    def robots_txt(self):
        pass

    # param browser object of the page
    # return a list of categories as browser objects
    def get_cats(self):
        if self.url == "https://www.hisco.com/product-index":
            cats = self.browser.find_elements_by_css_selector("div.row > div > div.widget-richcontent > p")
            print(len(cats), self.url)
            return cats
        print("subs", self.url)

    # param browser object of a category tag
    # return the name of the category as a string
    def get_cat_name(self, cat):
        cat_name = ""
        names = cat.find_elements_by_css_selector("a")
        print(len(cat_name))
        return cat_name

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
        pass

    # param browser object of the page
    # return a list of products as browser objects
    def get_prods(self):
        pass

    # param browser object of the item to be scraped
    # return item description as a string
    def get_item_desc(self, item):
        pass

    # param browser object of the item to be scraped
    # return item link as a string
    def get_item_link(self, item):
        pass

    # param browser object of the item to be scraped
    # return item image as a string
    def get_item_image(self, item):
        pass

    # param browser object of the item to be scraped
    # return item price as a string
    def get_item_price(self, item):
        pass

    # param browser object of the item to be scraped
    # return unit that the item is sold in as string ("box of 10")
    def get_item_unit(self, item):
        pass

    # param browser object of the item being scrapped
    # return all the specs of the item are returned as a string with the format {'key' : 'val'}
    def get_item_specs(self, item):
        pass
