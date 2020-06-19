import Site as st
import json
import time
from bs4 import BeautifulSoup


class MartinSupplyCrawler(st.Site):

    # return terms of service else None
    def terms_of_service(self):
        return None


    # return robots.txt else None
    def robots_txt(self):
        return None

    # return a list of categories as a list of soup objects
    def get_cats(self):
        if(self.url == "https://shop.martinsupply.com/store/categoryList.cfm"):
            return self.browser.find_elements_by_css_selector("#category > ul > li")[1:]
        else:
            cat_list = self.browser.find_elements_by_css_selector("#category > ul > li")
            res_list = []
            for cat in cat_list:
                if("view all" not in self.get_cat_name(cat).lower()):
                    res_list.append(cat)
            return res_list


    # param browser object of a category tag
    # return the name of the category as a string
    def get_cat_name(self, cat):
        return cat.find_element_by_css_selector("h3 > a").text

    # param browser object of the page
    # return the link to the show all page as a string if it exits
    # else return None
    def get_show_all_page(self):
        return None

    # param browser object of the page
    # return a list of pages of products as browser objects
    # else return None
    def get_prod_pages(self):
        return None

    # param browser object of the page
    # return the next page of products as a browser object
    # else return None
    def get_next_page(self):
        return self.browser.find_element_by_css_selector("a.prevEndNextN").get_attribute("href")

    # param browser object of the page
    # return a list of products as browser objects
    def get_prods(self):
    	return self.browser.find_elements_by_css_selector("#product > ul > li")

    # param browser object of the item to be scraped
    # return item description as a string
    def get_item_desc(self, item):
    	return item.find_element_by_css_selector("h3 > a").text.strip()

    # param browser object of the item to be scraped
    # return item link as a string
    def get_item_link(self, item):
    	return item.find_element_by_css_selector("h3 > a").get_attribute("href")

    # param browser object of the item to be scraped
    # return item image as a string
    def get_item_image(self, item):
        img = None
        try:
            img = item.find_element_by_css_selector("img.productlist_product").get_attribute("src")
        except:
            pass 
        return img

    # param browser object of the item to be scraped
    # return item price as a string
    def get_item_price(self, item):
        price = None
        old_url = self.url
        self.follow_url(self.get_item_link(item))
        try:
            price = self.browser.find_element_by_css_selector("div.cart-cost").text.strip()
        except:
            pass
        self.follow_url(old_url)
        return price



    # param browser object of the item to be scraped
    # return unit that the item is sold in as string ("box of 10")
    def get_item_unit(self, item):
        unit = None
        old_url = self.url
        self.follow_url(self.get_item_link(item))
        try:
            unit_whole = self.browser.find_elements_by_css_selector("div.cart-option")[-1]
            unit_first = unit_whole.find_element_by_css_selector("strong").text.strip()
            unit = unit_whole.text.strip().replace(unit_first, "").strip()
        except:
            pass
        self.follow_url(old_url)
        return unit



    # param browser object of the item being scrapped
    # return all the specs of the item are returned as a string with the format {'key' : 'val'}
    def get_item_specs(self, item=None):
        res = {}
        specs = self.browser.find_elements_by_css_selector("div.cart-option")[:-1]
        for spec in specs:
            key = spec.find_element_by_css_selector("strong").text.strip().replace(":", "")
            val = spec.text.strip().replace(key, "").strip()
            
            res[key] = val

        return json.dumps(res)

