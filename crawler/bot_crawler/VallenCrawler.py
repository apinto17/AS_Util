import Site as st
import json
import time
from bs4 import BeautifulSoup
import re


class VallenCrawler(st.Site):

    # return terms of service else None
    def terms_of_service(self):
        pass

    # return robots.txt else None
    def robots_txt(self):
        pass

    # param browser object of the page
    # return a list of categories as browser objects
    def get_cats(self):
        if self.url == "https://www.vallen.com/categories":
            return self.browser.find_elements_by_css_selector("a.text-info")

    # param browser object of a category tag
    # return the name of the category as a string
    def get_cat_name(self, cat):
        if self.url == "https://www.vallen.com/categories":
            prim_cat = self.browser.find_element_by_css_selector("a.ng-binding").text
            print(prim_cat + "|" + cat.text)
            return prim_cat + "|" + cat.text

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
        # Vallen's product pages are unique, they're closer to an "endless" feed than a paginated list.
        # The "Load More" button loads 5 items.
        # Click the "Load More" button until disappears, which means we have all the products.
        while (
            len(
                self.browser.find_elements_by_css_selector(
                    "button[class='btn btn-secondary btn-lg no-animate ng-scope']"
                )
            )
            > 0
        ):
            load_more_button = self.browser.find_element_by_css_selector(
                "button[class='btn btn-secondary btn-lg no-animate ng-scope']"
            )

            load_more_button.click()
            time.sleep(1)

        prods = self.browser.find_elements_by_css_selector("div.result-item-block")
        return prods
    
    # param browser object of the item to be scraped
    # return item description as a string
    def get_item_desc(self, item):
        return item.find_element_by_css_selector("a.prod-name").text.strip()

    # param browser object of the item to be scraped
    # return item link as a string
    def get_item_link(self, item):
        href = item.find_element_by_css_selector("a.prod-name").get_attribute("href")
        print("href", href)
        return href

    # param browser object of the item to be scraped
    # return item image as a string
    def get_item_image(self, item):
        print("get_item_image", self.url)
        pass

    # param browser object of the item to be scraped
    # return item price as a string
    def get_item_price(self, item):
        print("get_item_price", self.url)
        pass

    # param browser object of the item to be scraped
    # return unit that the item is sold in as string ("box of 10")
    def get_item_unit(self, item):
        print("get_item_unit", self.url)
        pass

    # param browser object of the item being scrapped
    # return all the specs of the item are returned as a string with the format {'key' : 'val'}
    def get_item_specs(self, item):
        res = {}
        if item is None:
            return json.dumps(res)
        soup = BeautifulSoup(item.get_attribute("innerHTML"), "html.parser")
        print("get_item_specs", self.url)
        pass
