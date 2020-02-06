
import generalized_link_crawler as gc
import json

class bhid_crawler(gc.Site):


    # return terms of service else None
    
    def terms_of_service(self):
        return None


    # return robots.txt else None
    
    def robots_txt(self):
        return None


    # param browser object of the page
    # return a list of categories as browser objects
    
    def get_cats(self):
        return self.soup.select("div.cat-list > ul > li")

    # param browser object of a category tag
    # return the name of the category as a string
    
    def get_cat_name(self, cat):
    	pass

    # param bs object containing a category
    # return the link for that category
    
    def get_cat_link(self, cat):
    	pass

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

    # return the link for the given prod page
    
    def get_prod_page_link(self, page):
    	pass


    # return the link of the next page button
    
    def get_next_page_link(self):
        pass

    # param browser object of the page
    # return a list of products as browser objects
    
    def get_prods(self):
    	pass

    # param browser object of the item to be scraped
    # return item description as a string
    
    def get_item_desc(self, item):
    	pass

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
