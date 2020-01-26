
import generalized_link_crawler as gc
import json
import re



class kele_crawler(gc.Site):

    # return terms of service else None
    def terms_of_service(self):
        pass


    # return robots.txt else None
    def robots_txt(self):
        pass


    # param browser object of the page
    # return a list of categories as browser objects
    def get_cats(self):
        if(self.url == "https://www.kele.com/product-categories.aspx"):
            return self.soup.select("a.categories-category")
        elif(len(self.soup.select("div.product-sub-categories > ul > li")) > 0):
            return self.soup.select("div.product-sub-categories > ul > li")
        else:
            return self.soup.select("#ctl00_ctl00_cphM1_cphMM1_tblList > tbody > tr > td")

    # param browser object of a category tag
    # return the name of the category as a string
    def get_cat_name(self, cat):
        return cat.select_one("span.categories-category-title").text

    # param bs object containing a category
    # return the link for that category
    def get_cat_link(self, cat):
        return cat.select_one("a")['href']

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

    # return the link for the given prod page
    def get_prod_page_link(self, page):
        return None


    # return the link of the next page button
    def get_next_page_link(self):
        return None

    # param browser object of the page
    # return a list of products as browser objects
    def get_prods(self):
        return self.soup.select("#pTab > tbody tr")

    # param browser object of the item to be scraped
    # return item description as a string
    def get_item_desc(self, item):
        return item.select_one("td.DescrCol").text.strip()

    # param browser object of the item to be scraped
    # return item link as a string
    def get_item_link(self, item):
        return None

    # param browser object of the item to be scraped
    # return item image as a string
    def get_item_image(self, item):
        return None

    # param browser object of the item to be scraped
    # return item price as a string
    def get_item_price(self, item):
        return item.select_one("td.OnlineCol").text

    # param browser object of the item to be scraped
    # return unit that the item is sold in as string ("box of 10")
    def get_item_unit(self, item):
        return None

    # param browser object of the item being scrapped
    # return all the specs of the item are returned as a string with the format {'key' : 'val'}
    def get_item_specs(self, item=None):
        return None