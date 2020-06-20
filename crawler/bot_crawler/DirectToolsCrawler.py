import Site as st
import json
import time
from bs4 import BeautifulSoup


class DirectToolsCrawler(st.Site):

    # return terms of service else None
    def terms_of_service(self):
        return None

    # return robots.txt else None
    def robots_txt(self):
        return None

    # return a list of categories as a list of soup objects
    def get_cats(self):
        return self.browser.find_elements_by_css_selector("div.sub-category > a")

    # param browser object of a category tag
    # return the name of the category as a string
    def get_cat_name(self, cat):
        return cat.text

    # param browser object of the page
    # return the link to the show all page as a string if it exits
    # else return None
    def get_show_all_page(self):
        return self.browser.find_element_by_css_selector(
            "nav.column > ul > li:nth-last-child(1) > a"
        )

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
        return self.browser.find_elements_by_css_selector("div.category-product > a")

    # param browser object of the item to be scraped
    # return item description as a string
    def get_item_desc(self, item):
        return item.find_element_by_css_selector("p").text.strip()

    # param browser object of the item to be scraped
    # return item link as a string
    def get_item_link(self, item):
        return item.get_attribute("href")

    # param browser object of the item to be scraped
    # return item image as a string
    def get_item_image(self, item):
        img = None
        try:
            img = item.find_element_by_css_selector("span.imgh > img").get_attribute(
                "src"
            )
        except:
            pass
        return img

    # param browser object of the item to be scraped
    # return item price as a string
    def get_item_price(self, item):
        return item.find_element_by_css_selector("strong").text

    # param browser object of the item to be scraped
    # return unit that the item is sold in as string ("box of 10")
    def get_item_unit(self, item):
        return ""

    # param browser object of the item being scrapped
    # return all the specs of the item are returned as a string with the format {'key' : 'val'}
    def get_item_specs(self, item=None):
        res = {}
        try:
            specs_header = self.browser.find_element_by_xpath(
                "//*[contains(text(), 'Specifications')]"
            )
            specs = specs_header.find_element_by_xpath("./following-sibling::ul")
            specs = specs.find_elements_by_css_selector("li")
            for spec in specs:
                spec_list = spec.text.strip().split(":")
                res[spec_list[0]] = spec_list[1]
        except:
            pass
        return json.dumps(res)
