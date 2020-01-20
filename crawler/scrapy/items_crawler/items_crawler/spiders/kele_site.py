
from .site import Site
import json


class Kele(Site):

    # return terms of service else None

    def terms_of_service(self, response):
        return None


    # return robots.txt else None

    def robots_txt(self, response):
        return None


    # param browser object of the page
    # return a list of categories as browser objects

    def get_cats(self, response):
        return response.css("li.category-li")


    # param bs object containing a category
    # return the link for that category

    def get_cat_link(self, cat, response):
        if(response.url == "https://www.bhid.com/"):
            return self.header + cat.css("a").attrib["href"]
        else:
            return self.header + cat.css("div.categorycontent-text > a").attrib["href"]

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

    # return the link for the given prod page

    def get_prod_page_link(self, page):
    	return None


    # return the link of the next page button

    def get_next_page_link(self, response):
        next_page = response.css("div.SearchResultPaging > a")[-1]
        if("NEXT" in next_page.css("::text").get()):
            return self.header + next_page.attrib["href"]
        else:
            return None

    # param browser object of the page
    # return a list of products as browser objects

    def get_prods(self, response):
    	return response.css("div.SKULineWrapper")


    def get_cat_string(self, response):
        res = ""
        cats = response.css("div.SearchResultsLblInfo > span > a::text").getall()
        cats.append(response.css("div.SearchResultsLblInfo > span > span::text").get())
        for cat in cats:
            cat = cat[:-1]
            if(len(cat) > 0):
                res += "|" + cat

        return res


    # param browser object of the item to be scraped
    # return item description as a string

    def get_item_desc(self, item):
        return item.css("div.SKULineDescInfo > h2 > a::text").get()

    # param browser object of the item to be scraped
    # return item link as a string

    def get_item_link(self, item):
    	return self.header + item.css("div.SKULineDescInfo > h2 > a").attrib['href']

    # param browser object of the item to be scraped
    # return item image as a string

    def get_item_image(self, item):
        return self.header + item.css("div.sku-image-enlarge > a").attrib['href']

    # param browser object of the item to be scraped
    # return item price as a string

    def get_item_price(self, item):
    	return item.css("span.PriceBreaks::text").get()

    # param browser object of the item to be scraped
    # return unit that the item is sold in as string ("box of 10")

    def get_item_unit(self, item):
    	return item.css("span.SKULineUOM").attrib['data-uom']

    # param browser object of the item being scrapped
    # return all the specs of the item are returned as a string with the format {'key' : 'val'}

    def get_item_specs(self, item):
        res = {}
        specs = item.css("div.item-specs > ul > li")
        for spec in specs:
            key = spec.css("label::text").get()[:-2].strip()
            val = spec.css("div.itemSpecValues::text").get().strip()
            res[key] = val
        return json.dumps(res)