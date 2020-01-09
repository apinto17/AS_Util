
from .site import Site


class AutoDirect(Site):

    # return terms of service else None

    def terms_of_service(self, response):
        return None


    # return robots.txt else None

    def robots_txt(self, response):
        return None


    # param browser object of the page
    # return a list of categories as browser objects

    def get_cats(self, response):
        if(response.url == "https://www.automationdirect.com/adc/home/home"):
            return response.css("#ptItems > ul > li")[:-2]
        else:
            cats = response.css("div.categoryIndexWrapper > div")
            if(cats.css("a.selectedItemLink") != []):
                return None 
            else:
                return cats


    # param browser object of a category tag
    # return the name of the category as a string

    def get_cat_name(self, cat):
        return cat.css("a > span::text").get()

    # param bs object containing a category
    # return the link for that category

    def get_cat_link(self, cat):
    	return self.header + cat.css("a").attrib['href']

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
    	pass


    # return the link of the next page button

    def get_next_page_link(self, response):
        return None

    # param browser object of the page
    # return a list of products as browser objects

    def get_prods(self, response):
    	return response.css("#productListTable > div")

    # param browser object of the item to be scraped
    # return item description as a string

    def get_item_desc(self, item):
    	item.css("div.short-description > p > a::text")

    # param browser object of the item to be scraped
    # return item link as a string

    def get_item_link(self, item):
    	pass

    # param browser object of the item to be scraped
    # return item image as a string

    def get_item_image(self, item):
    	pass

    # param browser object of the item to be scraped
    # return item price as a string

    def get_item_price(self, item):
    	pass

    # param browser object of the item to be scraped
    # return unit that the item is sold in as string ("box of 10")

    def get_item_unit(self, item):
    	pass

    # param browser object of the item being scrapped
    # return all the specs of the item are returned as a string with the format {'key' : 'val'}

    def get_item_specs(self, item):
        pass