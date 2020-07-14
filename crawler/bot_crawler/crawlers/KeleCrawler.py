from bot_crawler import Site as st
import time
from bs4 import BeautifulSoup


class KeleCrawler(st.Site):

    # return terms of service else None
    def terms_of_service(self):
        return None

    # return robots.txt else None
    def robots_txt(self):
        return None

    # return a list of categories as a list of soup objects
    def get_cats(self):
        if self.url == "https://www.kele.com/product-categories.aspx":
            return self.browser.find_elements_by_css_selector("a.categories-category")
        else:
            subs = self.browser.find_elements_by_css_selector("div.product-sub-categories > ul > li > a")
            return subs

    # param browser object of a category tag
    # return the name of the category as a string
    def get_cat_name(self, cat):
        cat_name = ""
        try:
            cat_name = cat.find_element_by_css_selector("p").text
        except:
            cat_name = cat.text
        return cat_name

    # param browser object of the page
    # return the link to the show all page as a string if it exits
    # else return None
    def get_show_all_page(self):
        return None

    # param browser object of the page
    # return a list of pages of products as browser objects
    # else return None
    def get_prod_pages(self):
        return self.browser.find_elements_by_css_selector("span.paginate_button")[1:-1]

    # param browser object of the page
    # returns a list of product categories
    # else return None
    def get_prod_cats(self):
        return self.browser.find_elements_by_css_selector("a.prodlistMoreLink")

    # param browser object of the page
    # return the next page of products as a browser object
    # else return None
    def get_next_page(self):
        return None

    # param browser object of the page
    # return a list of products as browser objects
    def get_prods(self):
        return self.browser.find_elements_by_css_selector("#pTab > tbody > tr")

    # param browser object of the item to be scraped
    # return item description as a string
    def get_item_desc(self, item):
        return item.find_element_by_css_selector("td.DescrCol").text

    # param browser object of the item to be scraped
    # return item link as a string
    def get_item_link(self, item):
        return self.browser.current_url

    # param browser object of the item to be scraped
    # return item image as a string
    def get_item_image(self, item):
        return None

    # param browser object of the item to be scraped
    # return item price as a string
    def get_item_price(self, item):
        return item.find_element_by_css_selector("td.OnlineCol").text

    # param browser object of the item to be scraped
    # return unit that the item is sold in as string ("box of 10")
    def get_item_unit(self, item):
        return "EA"

    # param browser object of the item being scrapped
    # return all the specs of the item are returned as a string with the format {'key' : 'val'}
    def get_item_specs(self, item=None):
        return json.dumps({})