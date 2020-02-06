
from .site import Site
import json


class Bhid(Site):

    # return terms of service else None

    def terms_of_service(self, response):
        return None


    # return robots.txt else None

    def robots_txt(self, response):
        return None


    # param browser object of the page
    # return a list of categories as browser objects

    def get_cats(self, response):
        return response.css("div.cat-list > ul > li")[1:]


    # param bs object containing a category
    # return the link for that category

    def get_cat_link(self, cat, response):
        return self.header + cat.css("a").attrib["href"]

    # param browser object of the page
    # return the link to the show all page as a string if it exits
    # else return None

    def get_show_all_page(self, response):
    	return None

    # param browser object of the page
    # return a list of pages of products as browser objects
    # else return None

    def get_prod_pages(self, response):
    	return None


    # return the link of the next page button

    def get_next_page_selector(self):
        return "div.page-next"

    # param browser object of the page
    # return a list of products as browser objects

    def get_prods(self, response):
    	return response.css("li.item-block")


    def get_cat_string(self, response):
        res = ""
        cats = response.css("ul.breadcrumbs > li > a::text").getall()[2:]
        for cat in cats:
            if(len(cat) > 0):
                res += "|" + str(cat)

        return res


    # param browser object of the item to be scraped
    # return item description as a string

    def get_item_desc(self, item):
        return item.css("div.item-name > a::text").get()

    # param browser object of the item to be scraped
    # return item link as a string

    def get_item_link(self, item):
    	return self.header + item.css("div.item-name > a").attrib["href"]

    # param browser object of the item to be scraped
    # return item image as a string

    def get_item_image(self, item):
        return item.css("div.item-thumb > a > img").attrib["src"]

    # param browser object of the item to be scraped
    # return item price as a string

    def get_item_price(self, item):
    	return item.css("span.unit-net-price::text").get()

    # param browser object of the item to be scraped
    # return unit that the item is sold in as string ("box of 10")

    def get_item_unit(self, item):
    	return None

    # param browser object of the item being scrapped
    # return all the specs of the item are returned as a string with the format {'key' : 'val'}

    def get_item_specs(self, item):
        res = {}
        specs = []
        specs = item.css("table.spec-attributes > tbody > tr")
        for spec in specs:
            key = spec.css("td.col-label::text").get()
            value = spec.css("td.col-value::text").get()
            res[key] = value

        
        return json.dumps(res)
