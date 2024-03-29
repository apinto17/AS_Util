from bot_crawler import Site as st
import json
import time
from bs4 import BeautifulSoup


class BhidCrawler(st.Site):

    # return terms of service else None
    def terms_of_service(self):
        return None


    # return robots.txt else None
    def robots_txt(self):
        return None

    # return a list of categories as a list of soup objects
    def get_cats(self):
        if(self.url == "https://www.bhid.com/catalog/products"):
            cats = self.browser.find_elements_by_css_selector("li.products-category-card")[1:]
            return cats
        else:
            cats = self.browser.find_elements_by_css_selector("li.products-category-card")
            return cats

    # param browser object of a category tag
    # return the name of the category as a string
    def get_cat_name(self, cat):
        cat_name = cat.find_element_by_css_selector("h3.products-category-card__title").text
        #print("get_cat_name", cat_name)
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
        next_page = self.browser.find_element_by_css_selector("a[class='next-prev p-next']")
        #print("Found next page")
        return next_page

    # param browser object of the page
    # return a list of products as browser objects
    def get_prods(self):
        time.sleep(1)
        prods = self.browser.find_elements_by_css_selector("li.row")
        #print("prods", len(prods), self.url)
        return prods

    # param browser object of the item to be scraped
    # return item description as a string
    def get_item_desc(self, item):
        desc = item.find_element_by_css_selector("div.item-name > a").text.strip()
        #print("desc", desc, self.url)
        return desc

    # param browser object of the item to be scraped
    # return item link as a string
    def get_item_link(self, item):
        link = item.find_element_by_css_selector("div.item-name > a").get_attribute("href")
        #print("link", link)
        return link

    # param browser object of the item to be scraped
    # return item image as a string
    def get_item_image(self, item):
        img = None
        try:
            img = item.find_element_by_css_selector("img").get_attribute("src")
        except:
            pass
        #print("img", img)
        return img

    # param browser object of the item to be scraped
    # return item price as a string
    def get_item_price(self, item):
        price = item.find_element_by_css_selector("span.unit-net-price").text
        #print("price", price)
        return price

    # param browser object of the item to be scraped
    # return unit that the item is sold in as string ("box of 10")
    def get_item_unit(self, item):
        unit = None
        try:
            unit = item.find_element_by_css_selector("span.displayUnitOfMeasure").text
        except:
            pass
        #print("unit", unit)
        return unit

    # param browser object of the item being scrapped
    # return all the specs of the item are returned as a string with the format {'key' : 'val'}
    def get_item_specs(self, item=None):
        res = {}
        try:
            code = self.browser.page_source
            soup = BeautifulSoup(code, "html.parser")
            time.sleep(3)
            specs = soup.select("table > tbody > tr")
            for spec in specs:
                key = spec.select_one("td.col-label").text
                val = spec.select_one("td.col-value").text
                res[key] = val
        except Exception as e:
            pass
        return json.dumps(res) 

