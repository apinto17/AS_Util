from bot_crawler import Site as st
import json
import time
from bs4 import BeautifulSoup


class TannerCrawler(st.Site):

    # return terms of service else None
    def terms_of_service(self):
        return None


    # return robots.txt else None
    def robots_txt(self):
        return None

    # return a list of categories as a list of soup objects
    def get_cats(self):
        if(self.url == "https://www.tannerbolt.com/?page=customer&file=customer/tabonu/b2bse/includes/shop.aspx"):
            cats = self.browser.find_elements_by_css_selector("div.HomeCat > a")[:-1]
            return cats
        else:
            cats = self.browser.find_elements_by_css_selector("div.CategoryWrapper")
            return cats

    # param browser object of a category tag
    # return the name of the category as a string
    def get_cat_name(self, cat):
        try:
            cat_name = cat.find_element_by_css_selector("div.catname > p").text
        except:
            cat_name = cat.find_element_by_css_selector("a > div.CategoryTitle").text
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
        next_page = self.browser.find_element_by_css_selector("td.ItemSearchResults_PrevNextLinksTD > a.ItemSearchResults_PrevNextLinks")
        print("found next page")
        return next_page

    # param browser object of the page
    # return a list of products as browser objects
    def get_prods(self):
        prods = self.browser.find_elements_by_css_selector("div.Product")
        #print("prods", len(prods), self.url)
        return prods
    
    # param browser object of the item to be scraped
    # return item description as a string
    def get_item_desc(self, item):
        desc = item.find_element_by_css_selector("div.ProductInfoWrapper > div.ProductDesc > a.ItemDetailsLink > p").text
        #print(desc, self.url)
        return desc
    
    # param browser object of the item to be scraped
    # return item link as a string
    def get_item_link(self, item):
        link = item.find_element_by_css_selector("div.ProductInfoWrapper > div.ProductDesc > a.ItemDetailsLink").get_attribute("href")
        #print("link", link)
        return link

    # param browser object of the item to be scraped
    # return item image as a string
    def get_item_image(self, item):
        img = item.find_element_by_css_selector("div.ProductImgWrapper > img").get_attribute("src")
        #print("img", img)
        return img

    # param browser object of the item to be scraped
    # return item price as a string
    def get_item_price(self, item):
        price = item.find_element_by_css_selector("div.ProductDetails > span.Price").text
        #print("price", price)
        return price

    # param browser object of the item to be scraped
    # return unit that the item is sold in as string ("box of 10")
    def get_item_unit(self, item):
        unit = item.find_element_by_css_selector("div.UnitSizeWrapper > span.UnitSize").text
        #print("unit", unit, self.url)
        return unit
        
    # param browser object of the item being scrapped
    # return all the specs of the item are returned as a string with the format {'key' : 'val'}
    def get_item_specs(self, item=None):
        res = {}
        specs = self.browser.find_elements_by_css_selector("table.TechSpecs > tbody > tr")
        for spec in specs:
            key = spec.find_element_by_css_selector("td.AttrName").text 
            val = spec.find_element_by_css_selector("td.AttrValue").text
            if key != "" and val != "":
                res[key] = val
        return json.dumps(res)
