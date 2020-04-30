import sys
sys.path.append('../')


import crawler_util.crawler as c
import time


class Site():

    # url is the url you want to start at as a string
    # name is the display name of the site as a string
    # header is the beginning of the site url as a string ("www.abc.com/") can be blank if website
    #       uses absolute links
    def __init__(self, url, name, header):
        self.url = url
        self.name = name
        self.header = header
        self.server = None
        self.browser = None
        self.thread = -1
        super().__init__()

    def is_cat_page(self):
        try:
        	res = self.get_cats()
        	if(res != None and len(res) > 0):
        		return True
        	else:
        		return False
        except:
        	return False


    def is_prod_page(self):
        try:
            res = self.get_prods()
            if(res != None and len(res) > 0):
                return True
            else:
                return False
        except:
            return False


    def has_page_list(self):
        try:
        	res = self.get_prod_pages()
        	if(res != None and len(res) > 0):
        		return True
        	else:
        		return False
        except:
        	return False

    def has_page_turner(self):
        try:
            res = self.get_next_page()
            if(res != None):
                return True
            else:
                return False
        except:
        	return False


    def has_show_all_page(self):
        try:
        	res = self.get_show_all_page()
        	if(res != None):
        		return True
        	else:
        		return False
        except:
        	return False

    def specs_on_same_page(self, item):
        try:
        	res = self.get_item_specs(item)
        	if(res != None and res != '{}'):
        		return True
        	else:
        		return False
        except:
        	return False


    def follow_url(self, url):
        try:
            self.browser.get(url)
            self.url = url
        except:
            print("EXITING follow url")
            exit()
        time.sleep(c.SLEEP_TIME)

    # return terms of service else None
    def terms_of_service(self):
        pass


    # return robots.txt else None
    def robots_txt(self):
        pass

    # param browser object of the page
    # return a list of categories as browser objects
    def get_cats(self):
    	pass

    # param browser object of a category tag
    # return the name of the category as a string
    def get_cat_name(self, cat):
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

    # param browser object of the page
    # return the next page of products as a browser object
    # else return None
    def get_next_page(self):
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

