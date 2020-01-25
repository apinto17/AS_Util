
from .site import Site
import json


class Directtools(Site):

    # return terms of service else None

    def terms_of_service(self, response):
        return None


    # return robots.txt else None

    def robots_txt(self, response):
        return None


    # param browser object of the page
    # return a list of categories as browser objects

    def get_cats(self, response):
        return response.css("div.sub-category")


    # param bs object containing a category
    # return the link for that category

    def get_cat_link(self, cat, response):
        return cat.css("a").attrib["href"]

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

    def get_next_page_link(self, response):
        return response.css("a.page-links-next").attrib['href']

    # param browser object of the page
    # return a list of products as browser objects

    def get_prods(self, response):
    	return response.css("div.category-product")


    def get_cat_string(self, response):
        res = ""
        cats = response.css("div.row.breadcrumbs > nav > ul > li > a::text").getall()[2:]
        cats.append(response.css("span.current-item::text").get())
        for cat in cats:
            if(len(cat) > 0):
                res += "|" + str(cat)

        return res


    # param browser object of the item to be scraped
    # return item description as a string

    def get_item_desc(self, item):
        return item.css("a > p::text").get()

    # param browser object of the item to be scraped
    # return item link as a string

    def get_item_link(self, item):
    	return item.css("a").attrib['href']

    # param browser object of the item to be scraped
    # return item image as a string

    def get_item_image(self, item):
        return self.header + item.css("span.imgh > img").attrib["src"]

    # param browser object of the item to be scraped
    # return item price as a string

    def get_item_price(self, item):
    	return item.css("strong::text").get()

    # param browser object of the item to be scraped
    # return unit that the item is sold in as string ("box of 10")

    def get_item_unit(self, item):
    	return None

    # param browser object of the item being scrapped
    # return all the specs of the item are returned as a string with the format {'key' : 'val'}

    def get_item_specs(self, item):
        res = {}
        specs = []
        specs = item.css("td.prodDetSpecTable > table > tr")
        if(len(specs) > 0):
            for spec in specs:
                key = spec.css("td.prodDetSpecLeft::text").get()[:-1]
                val = spec.css("td.prodDetSpecrT::text").get()[:-1]
                res[key] = val
        else:
            specs = item.css("div.responsive-tabs > div > ul")[1].css("li::text").getall()
            for spec in specs:
                key = spec[:spec.index(":")]
                val = spec[spec.index(":") + 2:]
                res[key] = val          

        return json.dumps(res)
