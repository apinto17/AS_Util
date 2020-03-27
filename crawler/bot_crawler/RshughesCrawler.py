import GeneralizedCrawler as gc
import json
import time
from bs4 import BeautifulSoup


class RshughesCrawler(gc.Site):

    # return terms of service else None
    def terms_of_service(self):
        return None


    # return robots.txt else None
    def robots_txt(self):
        return None

    # return a list of categories as a list of soup objects
    def get_cats(self):
        if(self.url == "https://www.rshughes.com/"):
            return self.browser.find_elements_by_css_selector("ul.nav-l1 > li > a")
        else:
            return self.browser.find_elements_by_css_selector("tr.x-category-list > td")

    # param browser object of a category tag
    # return the name of the category as a string
    def get_cat_name(self, cat):
        if(self.url == "https://www.rshughes.com/"):
            return cat.find_element_by_css_selector("a > span").text
        else:
            return cat.find_element_by_css_selector("div.category-iconic-name").text

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
        return self.browser.find_element_by_css_selector("a[title='Next Page']")

    # param browser object of the page
    # return a list of products as browser objects
    def get_prods(self):
    	return self.browser.find_elements_by_css_selector("div[class='x-products x-view-grid'] > *.x-product")

    # param browser object of the item to be scraped
    # return item description as a string
    def get_item_desc(self, item):
    	return item.find_element_by_css_selector("a.x-link-name").text.strip()

    # param browser object of the item to be scraped
    # return item link as a string
    def get_item_link(self, item):
    	return item.find_element_by_css_selector("a.x-link-name").get_attribute("href")

    # param browser object of the item to be scraped
    # return item image as a string
    def get_item_image(self, item):
        img = None
        try:
            img = item.find_element_by_css_selector("img").get_attribute("src")
        except:
            pass 
        return img

    # param browser object of the item to be scraped
    # return item price as a string
    def get_item_price(self, item):
        price_str = item.find_element_by_css_selector("span.x-price").text
        return price_str.split(" ")[0]

    # param browser object of the item to be scraped
    # return unit that the item is sold in as string ("box of 10")
    def get_item_unit(self, item):
        price_str = item.find_element_by_css_selector("span.x-price").text
        if(len(price_str.split(" ")) < 3):
            return ""
        else:
            return price_str.split(" ")[2]

    # param browser object of the item being scrapped
    # return all the specs of the item are returned as a string with the format {'key' : 'val'}
    def get_item_specs(self, item=None):
        res = {}
        specs = item.find_elements_by_css_selector("li.x-spec")
        for spec in specs:
            key = spec.find_element_by_css_selector("span.x-spec-name").text.replace(":", "")
            val = spec.find_element_by_css_selector("span.x-spec-value").text
            res[key] = val
        return json.dumps(res)

