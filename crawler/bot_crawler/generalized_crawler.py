import sys
sys.path.append('../')

from abc import ABC, abstractmethod

import crawler_util.crawler as c
import time
import re
import multiprocessing as mp

import logging
from crawler_util.server import Server



#                    _ooOoo_
#                   o8888888o
#                   88" . "88
#                   (| -_- |)
#                   O\  =  /O
#                ____/`---'\____
#              .'  \\|     |//  `.
#             /  \\|||  :  |||//  \
#            /  _||||| -:- |||||-  \
#            |   | \\\  -  /// |   |
#            | \_|  ''\---/''  |   |
#            \  .-\__  `-`  ___/-. /
#          ___`. .'  /--.--\  `. . __
#       ."" '<  `.___\_<|>_/___.'  >'"".
#      | | :  `- \`.;`\ _ /`;.`/ - ` : | |
#      \  \ `-.   \_ __\ /__ _/   .-` /  /
# ======`-.____`-.___\_____/___.-`____.-'======
#                    `=---='
#
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#           佛祖保佑           永无BUG
#          God Bless        Never Crash


def crawl_site(site, cats=""):

    c.sleep_counter(c.SLEEP_TIME)

    browser = c.get_headless_selenium_browser()
    try:
    	browser.get(site.url)
    except:
    	logging.critical(" URL " + site.url + " Categories:   " + cats, exc_info=True)
    	return

    DFS_on_categories(site, browser, cats)



# depth first search starting on the first category
def DFS_on_categories(site, browser, cats):
    if(cats == ""):
        FORMAT = '%(levelname)s: %(asctime)-15s %(message)s \n\n'
        logging.basicConfig(format=FORMAT, datefmt='%m/%d/%Y %I:%M:%S %p', filename=site.name + "/" + site.name + ".log",level=logging.DEBUG)
        site.server = Server()
        site.server.connect()

    if(site.is_cat_page(browser)):

        for i in range(len(site.get_cats(browser))):

            c.sleep_counter(c.SLEEP_TIME)

            # update list
            cat_list = site.get_cats(browser)
            cats += "|" + site.get_cat_name(cat_list[i])
            print(site.get_cat_name(cat_list[i]))
            print(browser.current_url)

            # click on category
            prev_url = browser.current_url
            click_on_page(browser, site, cat_list[i])

            # depth first search on category
            try:
                logging.info(" URL " + site.url + " Categories:   " + cats)
                DFS_on_categories(site, browser, cats)
            except:
                logging.error(" URL " + site.url + " Categories:   " + cats, exc_info=True)

            # restory previous browser
            site.url = prev_url
            browser.get(prev_url)

    elif(site.is_prod_page(browser)):
        print("Scrapping page")
        print(browser.current_url)
        scrape_page(site, browser, cats)

    else:
        raise ValueError("Unable to crawl page")
        return


def click_on_page(browser, site, page):

    browser.execute_script("return arguments[0].scrollIntoView();", page)
    time.sleep(1)
    page.click()
    site.url = browser.current_url


# go through every page and scrape info
def scrape_page(site, browser, cats):

    # scrape show all page if it exits
    if(site.has_show_all_page(browser)):
        c.sleep_counter(c.SLEEP_TIME)
        site.get_show_all_page(browser).click()
        get_prods_info(site, browser, cats)

    # else if there is a page list, scape pages
    elif(site.has_page_list(browser)):

        c.sleep_counter(c.SLEEP_TIME)
        # scrape products on the first page
        get_prods_info(site, browser, cats)

        # scrape products on subsequent pages
        for i in range(len(site.get_prod_pages(browser))):

            c.sleep_counter(c.SLEEP_TIME)

            page_list = site.get_prod_pages(browser)

            prev_url = browser.current_url
            click_on_page(browser, site, page_list[i])

            get_prods_info(site, browser, cats)

            site.url = prev_url
            browser.get(prev_url)

    # else if the site only has a page turner
    elif(site.has_page_turner(browser)):
        c.sleep_counter(c.SLEEP_TIME)
        # scrape products on the first page
        get_prods_info(site, browser, cats)

        # scrape subsequent pages
        while(True):
            c.sleep_counter(c.SLEEP_TIME)

            click_on_page(browser, site, site.get_next_page(browser))

            get_prods_info(site, browser, cats)

            if(not site.has_page_turner(browser)):
                break

    # else scrape the page
    else:
        c.sleep_counter(c.SLEEP_TIME)
        get_prods_info(site, browser, cats)


def get_prods_info(site, browser, cats):
    item_num = 1
    for i in range(len(site.get_prods(browser))):
        prod_list = site.get_prods(browser)
        try:
            get_item_info(site, browser, prod_list[i], cats)
        except:
            logging.error("COULDN'T SCRAPE ITEM NUMBER " + str(item_num) + " URL " + site.url + " Categories:   " + cats, exc_info=True)

        item_num += 1



def get_item_info(site, browser, item, cats):
    desc = site.get_item_desc(item)
    link = site.header + site.get_item_link(item)
    img = site.get_item_image(item)
    price = site.get_item_price(item)
    unit = site.get_item_unit(item)
    sitename = site.name
    specs = get_specs(site, item, browser)

    res_dict = {"Desc" : desc, "Link" : link, "Image" : img, "Price" : price, "Unit" : unit, "Sitename" : sitename, "Categories" : cats[1:], "Specs" : specs}

    site.server.write_to_db(desc, link, img, price, unit, sitename, cats[1:], specs)

    res_dict["Desc"] = unidecode.unidecode(res_dict["Desc"])
    logging.info("Thread: " + str(site.thread) + " " + str(res_dict))



def get_specs(site, item, browser):

    specs = None
    if(site.has_specs_link(item)):
        prev_url = browser.current_url
        browser.get(site.get_item_link(item))
        specs = site.get_item_specs(browser)
        browser.get(prev_url)
    else:
        specs = site.get_item_specs(item)

    return specs



def test(site, link, func, arg):

    site.url = link

    if(type(arg) is not str):
        raise ValueError("Fourth argument must be a String")

    elif(arg.lower() == "browser"):
        browser = c.get_headless_selenium_browser()
        browser.get(link)

        res = func(browser)

        print(res)
        if(type(res) == list):
            for val in res:
                print("----------------------------------------")
                print(val.text)
        else:
            print("----------------------------------------")
            print(res.text)
            print("----------------------------------------")

    elif(arg.lower() == "cat"):
        browser = c.get_headless_selenium_browser()
        browser.get(link)

        if(not site.is_cat_page(browser)):
            raise ValueError("Second argument must be the link for the page of categories")
        cats = site.get_cats(browser)
        for cat in cats:
            print("----------------------------------------")
            print(func(cat))

    elif(arg.lower() == "item"):
        browser = c.get_headless_selenium_browser()
        browser.get(link)

        if(not site.is_prod_page(browser)):
            raise ValueError("Second argument must be the link for the page of products")

        for item in site.get_prods(browser):
            print("----------------------------------------")
            print(func(item))

    else:
        raise ValueError("Fourth argument not recognized, must be either \"browser\", \"cat\", or \"item\"")



def main():
    pass



class Site(ABC):

    # url is the url you want to start at as a string
    # name is the display name of the site as a string
    # header is the beginning of the site url as a string ("www.abc.com/") can be blank if website
    #       uses absolute links
    def __init__(self, url, name, header):
        self.url = url
        self.name = name
        self.header = header
        self.server = None
        super().__init__()

    def is_cat_page(self, browser):
        try:
        	res = self.get_cats(browser)
        	if(res != None and res != []):
        		return True
        	else:
        		return False
        except:
        	return False


    def is_prod_page(self, browser):
        try:
        	res = self.get_prods(browser)
        	if(res != None and res != []):
        		return True
        	else:
        		return False
        except:
        	return False


    def has_page_list(self, browser):
        try:
        	res = self.get_prod_pages(browser)
        	if(res != None and res != []):
        		return True
        	else:
        		return False
        except:
        	return False

    def has_page_turner(self, browser):
        try:
        	res = self.get_next_page(browser)
        	if(res != None and res != []):
        		return True
        	else:
        		return False
        except:
        	return False


    def has_show_all_page(self, browser):
        try:
        	res = self.get_show_all_page(browser)
        	if(res != None):
        		return True
        	else:
        		return False
        except:
        	return False

    def has_specs_link(self, item):
        try:
        	res = self.get_item_link(item)
        	if(res != None):
        		return True
        	else:
        		return False
        except:
        	return False

    # param browser object of the page
    # return a list of categories as browser objects
    @abstractmethod
    def get_cats(self, browser):
    	pass

    # param browser object of a category tag
    # return the name of the category as a string
    @abstractmethod
    def get_cat_name(self, cat):
    	pass

    # param browser object of the page
    # return the link to the show all page as a string if it exits
    # else return None
    @abstractmethod
    def get_show_all_page(self, browser):
    	pass

    # param browser object of the page
    # return a list of pages of products as browser objects
    # else return None
    @abstractmethod
    def get_prod_pages(self, browser):
    	pass

    # param browser object of the page
    # return the next page of products as a browser object
    # else return None
    @abstractmethod
    def get_next_page(self, browser):
        pass

    # param browser object of the page
    # return a list of products as browser objects
    @abstractmethod
    def get_prods(self, browser):
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


if(__name__ == "__main__"):
	main()
