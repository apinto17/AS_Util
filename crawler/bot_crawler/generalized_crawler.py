import sys
sys.path.append('../')

from abc import ABC, abstractmethod

import crawler_util.crawler as c
import time
import re
import multiprocessing as mp

import logging
from crawler_util.server import Server
import os
import unidecode
import math


import bhid_crawler as bh



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


SLEEP_TIME = 1
NUM_PROCESSES = 10


def crawl_site(site):
    # make folder
    if(not os.path.isdir(site.name)):
        os.mkdir(site.name)

    home_url = site.url

    # get terms of service and robots.txt
    site.browser = c.get_headless_selenium_browser()
    site.follow_url(site.url)
    terms_file = open(site.name + "/" + site.name + "_terms_of_service.txt", "w+")
    robots_file = open(site.name + "/" + site.name + "_robots.txt", "w+")
    tos = site.terms_of_service()
    rob = site.robots_txt()
    if(tos is not None):
        terms_file.write(tos)
    if(rob is not None):
        robots_file.write(rob)

    site.url = home_url
    site.follow_url(site.url)

    # split processes and crawl
    p = mp.Pool(NUM_PROCESSES)
    arg_list = get_arg_list(site)

    p.map(multi_run_wrapper, arg_list)
    p.terminate()
    p.join()


def multi_run_wrapper(args):
    DFS_on_categories(*args)
    


def get_arg_list(site):
    arg_list = []
    cat_adder = math.floor(len(site.get_cats()) / NUM_PROCESSES)
    start = 0
    end = start + cat_adder

    for i in range(NUM_PROCESSES):
        if (i == NUM_PROCESSES - 1):
            end = -1
        new_site = bh.bhid_crawler(site.url, site.name, site.header)
        new_site.thread = i
        arg_list.append((new_site, "", start, end))
        start += cat_adder
        end += cat_adder

    return arg_list




# depth first search starting on the first category
def DFS_on_categories(site, cats, start=-1, end=-1):
    if(cats == ""):
        init(site, start, end)

    if(site.is_cat_page()):
        old_cats = cats
        prim_cat_list = get_cat_list(site, start, end)
        counter = 0
        for i in range(len(prim_cat_list)):
            time.sleep(SLEEP_TIME)
            # update list
            cat_list = get_cat_list(site, start, end)
            cats += "|" + site.get_cat_name(cat_list[i])

            # click on category
            prev_url = site.browser.current_url
            click_on_page(site, cat_list[i])

            # depth first search on category
            try:
                logging.info("Thread: " + str(site.thread) + " URL " + site.url + " Categories:   " + cats)
                DFS_on_categories(site, cats)
            except:
                logging.error("Thread: " + str(site.thread) + " URL " + site.url + " Categories:   " + cats, exc_info=True)

            # restory previous browser
            site.url = prev_url
            site.follow_url(prev_url)
            cats = old_cats
            counter += 1

        if(cats == ""):
            log_exit(counter, prim_cat_list, site)

    elif(site.is_prod_page()):
        scrape_page(site, cats)

    else:
        raise ValueError("Unable to crawl page")
        return


def get_cat_list(site, start, end):
    cat_list = site.get_cats()
    if(start != -1 and end != -1):
        cat_list = cat_list[start:end]
    elif(start != -1):
        cat_list = cat_list[start:]

    return cat_list


def init(site, start, end):
    site.browser = c.get_headless_selenium_browser()
    site.follow_url(site.url)
    FORMAT = '%(levelname)s: %(asctime)-15s %(message)s \n\n'
    logging.basicConfig(format=FORMAT, datefmt='%m/%d/%Y %I:%M:%S %p', filename=site.name + "/" + site.name + ".log",level=logging.DEBUG)
    site.server = Server()
    site.server.connect()
    logging.info("Thread: " + str(site.thread) + " start: " + str(start) + " end: " + str(end))


def log_exit(counter, prim_cat_list, site):
    if(counter == len(prim_cat_list)):
        logging.info("Thread " + str(site.thread) + " finished")
    else:
        logging.error("Thread " + str(site.thread) + " incomplete, missed " + str((len(prim_cat_list) - counter)) + " categories")




def click_on_page(site, page):
    site.browser.execute_script("return arguments[0].scrollIntoView();", page)
    time.sleep(1)
    page.click()
    site.url = site.browser.current_url


# go through every page and scrape info
def scrape_page(site, cats):
    # scrape show all page if it exits
    if(site.has_show_all_page()):      
        site.get_show_all_page().click()
        get_prods_info(site, cats)

    # else if there is a page list, scape pages
    elif(site.has_page_list()):      
        # scrape products on the first page
        get_prods_info(site, cats)

        # scrape products on subsequent pages
        for i in range(len(site.get_prod_pages())):

            page_list = site.get_prod_pages()

            prev_url = site.browser.current_url
            click_on_page(site, page_list[i])

            get_prods_info(site, cats)

            site.url = prev_url
            site.follow_url(prev_url)

    # else if the site only has a page turner
    elif(site.has_page_turner()):      
        # scrape products on the first page
        get_prods_info(site, cats)

        # scrape subsequent pages
        while(True):
            click_on_page(site, site.get_next_page())

            get_prods_info(site, cats)

            if(not site.has_page_turner()):
                break

    # else scrape the page
    else:        
        get_prods_info(site, cats)


def get_prods_info(site, cats):
    item_num = 1
    for i in range(len(site.get_prods())):
        time.sleep(SLEEP_TIME)
        prod_list = site.get_prods()

        try:
            get_item_info(site, prod_list[i], cats)
        except:
            logging.error("Thread: " + str(site.thread) + " COULDN'T SCRAPE ITEM NUMBER " + str(item_num) + " URL " + site.url + " Categories:   " + cats, exc_info=True)

        item_num += 1



def get_item_info(site, item, cats):
    desc = site.get_item_desc(item)
    link = site.get_item_link(item)
    img = site.get_item_image(item)
    price = site.get_item_price(item)
    unit = site.get_item_unit(item)
    sitename = site.name
    specs = get_specs(site, item)

    res_dict = {"Desc" : desc, "Link" : link, "Image" : img, "Price" : price, "Unit" : unit, "Sitename" : sitename, "Categories" : cats[1:], "Specs" : specs}

    site.server.write_to_db(desc, link, img, price, unit, sitename, cats[1:], specs)

    res_dict["Desc"] = unidecode.unidecode(res_dict["Desc"])
    logging.info("Thread: " + str(site.thread) + " " + str(res_dict))



def get_specs(site, item):

    specs = None
    if(site.specs_on_same_page(item)):
        specs = site.get_item_specs(item)
    else:
        prev_url = site.browser.current_url
        site.follow_url(site.get_item_link(item))
        
        specs = site.get_item_specs()
        site.follow_url(prev_url)
        

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
    bhid = bh.bhid_crawler("https://www.bhid.com/", "bhid.com", "https://www.bhid.com/")
    crawl_site(bhid)



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
        self.browser = None
        self.thread = -1
        super().__init__()

    def is_cat_page(self):
        try:
        	res = self.get_cats()
        	if(res != None and res != []):
        		return True
        	else:
        		return False
        except:
        	return False


    def is_prod_page(self):
        try:
        	res = self.get_prods()
        	if(res != None and res != []):
        		return True
        	else:
        		return False
        except:
        	return False


    def has_page_list(self):
        try:
        	res = self.get_prod_pages()
        	if(res != None and res != []):
        		return True
        	else:
        		return False
        except:
        	return False

    def has_page_turner(self):
        try:
        	res = self.get_next_page()
        	if(res != None and res != []):
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
            logging.critical("Thread: " + str(self.thread) + " URL " + self.url + "   Connection failed", exc_info=True)
            exit()
        time.sleep(SLEEP_TIME)



    # return terms of service else None
    def terms_of_service(self):
        pass


    # return robots.txt else None
    def robots_txt(self):
        pass

    # param browser object of the page
    # return a list of categories as browser objects
    @abstractmethod
    def get_cats(self):
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
    def get_show_all_page(self):
    	pass

    # param browser object of the page
    # return a list of pages of products as browser objects
    # else return None
    @abstractmethod
    def get_prod_pages(self):
    	pass

    # param browser object of the page
    # return the next page of products as a browser object
    # else return None
    @abstractmethod
    def get_next_page(self):
        pass

    # param browser object of the page
    # return a list of products as browser objects
    @abstractmethod
    def get_prods(self):
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
