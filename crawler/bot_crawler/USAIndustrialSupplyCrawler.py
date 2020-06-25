import Site as st
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
            return self.browser.find_elements_by_css_selector(
                "div[class='subcategories'] > li > a"
            )

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
        prods = self.browser.find_elements_by_css_selector("div.product-container")
        return prods

    # param browser object of the item to be scraped
    # return item description as a string
    def get_item_desc(self, item):
        desc = item.find_element_by_css_selector("div.product-info > a").text
        print("get_item_desc", desc, self.url)
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
        if(item is None):
            return json.dumps(res)
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
        }
        url = item.find_element_by_css_selector("a.product-title").get_attribute("href")
        req = requests.get(url, headers)
        soup = BeautifulSoup(req.content, 'html.parser')
        specs = soup.select(".wysiwyg-content ul li")
        for spec in specs:
            data = spec.text
            try:
                sep = data.split(":")
                res[sep[0]] = sep[1]
            except:
                res["Features"] = res.get("Features", "") + data + "\n"
        
        descs = soup.select(".wysiwyg-content p")
        for desc in descs:
            data = desc.text
            try:
                sep = data.split(":")
                res[sep[0]] = sep[1]
            except:
                res["Description"] = res.get("Description", "") + data + "\n"
        
        print(res, url)

        return json.dumps(res)
