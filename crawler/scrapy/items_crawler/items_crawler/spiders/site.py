
from abc import ABC, abstractmethod


class Site(ABC):

    # url is the url you want to start at as a string
    # name is the display name of the site as a string
    # header is the beginning of the site url as a string ("www.abc.com/") can be blank if website
    #       uses absolute links
    def __init__(self, url, name, header):
        self.url = url
        self.name = name
        self.header = header
        self.cats = ""
        super().__init__()


    def __repr__(self):
        return "(" + self.url + ", " + self.name + ", " + self.header + ")"


    def is_cat_page(self, response):
        try:
        	res = self.get_cats(response)
        	if(res != None and res != []):
        		return True
        	else:
        		return False
        except:
        	return False


    def is_prod_page(self, response):
        try:
        	res = self.get_prods(response)
        	if(res != None and res != []):
        		return True
        	else:
        		return False
        except:
        	return False


    def has_page_list(self, response):
        try:
        	res = self.get_prod_pages(response)
        	if(res != None and res != []):
        		return True
        	else:
        		return False
        except:
        	return False

    def has_page_turner(self, response):
        try:
            res = self.get_next_page_link(response)
            if(res != None and res != []):
            	return True
            else:
            	return False
        except:
        	return False


    def has_show_all_page(self, response):
        try:
        	res = self.get_show_all_page(response)
        	if(res != None):
        		return True
        	else:
        		return False
        except:
        	return False


    def specs_on_same_page(self, item):
        try:
        	res = self.get_item_specs(None, item)
        	if(res != None and res != '{}'):
        		return True
        	else:
        		return False
        except:
        	return False



    # return terms of service else None
    @abstractmethod
    def terms_of_service(self, response):
        pass


    # return robots.txt else None
    @abstractmethod
    def robots_txt(self, response):
        pass


    # param browser object of the page
    # return a list of categories as browser objects
    @abstractmethod
    def get_cats(self, response):
    	pass

    # param browser object of a category tag
    # return the name of the category as a string
    @abstractmethod
    def get_cat_name(self, cat, response):
    	pass

    # param bs object containing a category
    # return the link for that category
    @abstractmethod
    def get_cat_link(self, cat, response):
    	pass

    # param browser object of the page
    # return the link to the show all page as a string if it exits
    # else return None
    @abstractmethod
    def get_show_all_page(self, response):
    	pass

    # param browser object of the page
    # return a list of pages of products as browser objects
    # else return None
    @abstractmethod
    def get_prod_pages(self, response):
    	pass

    # return the link for the given prod page
    @abstractmethod
    def get_prod_page_link(self, page):
    	pass


    # return the link of the next page button
    @abstractmethod
    def get_next_page_link(self, response):
        pass

    # param browser object of the page
    # return a list of products as browser objects
    @abstractmethod
    def get_prods(self, response):
    	pass

    # param browser object of the item to be scraped
    # return item description as a string
    @abstractmethod
    def get_item_desc(self, item):
    	pass

    # param browser object of the item to be scraped
    # return item link as a string
    @abstractmethod
    def get_item_link(self, item):
    	pass

    # param browser object of the item to be scraped
    # return item image as a string
    @abstractmethod
    def get_item_image(self, item):
    	pass

    # param browser object of the item to be scraped
    # return item price as a string
    @abstractmethod
    def get_item_price(self, item):
    	pass

    # param browser object of the item to be scraped
    # return unit that the item is sold in as string ("box of 10")
    @abstractmethod
    def get_item_unit(self, item):
    	pass

    # param browser object of the item being scrapped
    # return all the specs of the item are returned as a string with the format {'key' : 'val'}
    @abstractmethod
    def get_item_specs(self, item):
        pass