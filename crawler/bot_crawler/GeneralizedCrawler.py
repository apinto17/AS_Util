import sys
sys.path.append('../')


import crawler_util.crawler as c
import time
import re
import multiprocessing as mp

import logging
from crawler_util.server import write_to_db
import os
import unidecode
import math
import AbstractCrawlerFactory as af
from selenium.webdriver.common.keys import Keys

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
#          God Bless        Never Crash

temp = set()
RETRY_COUNT = 30
logger = None
logger_missed_urls = None


def crawl_site(crawler_factory):
    site = crawler_factory.get_crawler()
    # make folder
    path_name = "logs/" + str(site.name)
    if(not os.path.isdir(path_name)):
        os.mkdir(folder_name)

    home_url = site.url

    # get terms of service and robots.txt
    site.browser = c.get_headless_selenium_browser()
    terms_file = open("logs/" + site.name + "/" + site.name + "_terms_of_service.txt", "w+")
    robots_file = open("logs/" + site.name + "/" + site.name + "_robots.txt", "w+")
    tos = site.terms_of_service()
    rob = site.robots_txt()
    if(tos is not None):
        terms_file.write(tos)
    if(rob is not None):
        robots_file.write(rob)

    site.url = home_url
    site.follow_url(site.url)

    # split processes and crawl
    p = mp.Pool(c.NUM_PROCESSES)
    arg_list = get_arg_list(site, crawler_factory)

    p.map(multi_run_wrapper, arg_list)
    p.terminate()
    p.join()


def multi_run_wrapper(args):
    DFS_on_categories(*args)
    

def get_arg_list(site, crawler_factory):
    arg_list = []
    cat_adder = math.floor(len(site.get_cats()) / c.NUM_PROCESSES)
    start = 0
    end = start + cat_adder

    for i in range(c.NUM_PROCESSES):
        if (i == c.NUM_PROCESSES - 1):
            end = -1

        new_site = crawler_factory.get_crawler()
        new_site.thread = i
        arg_list.append((new_site, "", start, end))
        start += cat_adder
        end += cat_adder

    return arg_list



# depth first search starting on the first category
def DFS_on_categories(site, cats, start=-1, end=-1):
    retry_count = 0
    if(cats == ""):
        init(site, start, end)

    while True:
        time.sleep(1)

        if(site.is_cat_page()):
            old_cats = cats
            prim_cat_list = get_cat_list(site, start, end)
            counter = 0
            for i in range(len(prim_cat_list)):
                time.sleep(c.SLEEP_TIME)
                # update list
                cat_list = get_cat_list(site, start, end)
                cats += "|" + site.get_cat_name(cat_list[i])

                # click on category
                prev_url = site.browser.current_url
                click_on_page(site, cat_list[i])

                # depth first search on category
                try:
                    logger.info("Thread: " + str(site.thread) + " URL " + site.url + " Categories:   " + cats)
                    DFS_on_categories(site, cats)
                except:
                    logger.error("Thread: " + str(site.thread) + " Missed URL " + site.url + " Categories:   " + cats, exc_info=True)
                    missed_urls_logger.info(site.url)

                # restory previous browser
                site.url = prev_url
                site.follow_url(prev_url)
                cats = old_cats
                counter += 1

            if(cats == ""):
                log_exit(counter, prim_cat_list, site)

        elif(site.is_prod_page()):
            scrape_page(site, cats)

        # A prod_cat page is a page with categories where each category
        # represents a single item with the same or very similar specs
        elif(site.is_prod_cat_page()):
            crawl_prod_cats(site, cats)

        elif(not site.is_prod_page() and not site.is_cat_page()):
            if retry_count > RETRY_COUNT:
                raise ValueError("Unable to crawl page")
                return
            else:
                retry_count += 1
                logger.info("Thread: " + str(site.thread) + " Retrying... {0}".format(retry_count))
        else:
            break


def get_cat_list(site, start, end):
    cat_list = site.get_cats()
    if(start != -1 and end != -1):
        cat_list = cat_list[start:end]
    elif(start != -1):
        cat_list = cat_list[start:]

    return cat_list


def setup_logger(name, log_file, level=logging.INFO):

    handler = logging.FileHandler(log_file)   
    FORMAT = '%(levelname)s: %(asctime)-15s %(message)s \n'
    formatter = logging.Formatter(fmt=FORMAT, datefmt='%m/%d/%Y %I:%M:%S %p')     
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


def init(site, start, end):
    global logger 
    global logger_missed_urls
    site.browser = c.get_headless_selenium_browser()
    site.follow_url(site.url)
    logger = setup_logger("info_logger", "logs/" + site.name + "/" + site.name + ".log")
    logger_missed_urls = setup_logger("missed_urls_logger", "logs/" + site.name + "/" + site.name + "_missed_urls.log")
    logger.info("Thread: " + str(site.thread) + " start: " + str(start) + " end: " + str(end))


def log_exit(counter, prim_cat_list, site):
    if(counter == len(prim_cat_list)):
        logger.info("Thread " + str(site.thread) + " finished")
    else:
        logger.error("Thread " + str(site.thread) + " incomplete, missed " + str((len(prim_cat_list) - counter)) + " categories")



def click_on_page(site, page):
    try:
        page = page.find_element_by_css_selector("a")
    except:
        pass 
    site.browser.execute_script("return arguments[0].scrollIntoView();", page)
    time.sleep(1)
    site.browser.execute_script("arguments[0].click();", page)
    site.url = site.browser.current_url


def crawl_prod_cats(site, cats):
    prod_cats = site.get_prod_cats()
    
    for i in range(len(prod_cats)): 
        prod_cats = site.get_prod_cats()
        prod_cat = prod_cats[i]
        click_on_page(site, prod_cat)
        retry_count = 0
        while(True):
            if(site.is_prod_page()):
                scrape_page(site, cats)
            else:
                if retry_count > RETRY_COUNT:
                    raise ValueError("Unable to crawl page")
                    return
                else:
                    retry_count += 1
                    logger.info("Thread: " + str(site.thread) + " Retrying... {0}".format(retry_count))


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
    crawled_items = []
    all_prods = site.get_prods()
    for i in range(len(all_prods)):
        time.sleep(c.SLEEP_TIME)
        prod_list = site.get_prods()

        try:
            item = (cats, site.get_item_desc(prod_list[i]))
            if(item not in crawled_items):
                get_item_info(site, prod_list[i], cats)
                crawled_items.append(item)
        except:
            logger.error("Thread: " + str(site.thread) + " COULDN'T SCRAPE ITEM NUMBER " + str(item_num) + " URL " + site.url + " Categories:   " + cats, exc_info=True)
            missed_urls_logger.info(site.url)




def get_item_info(site, item, cats):
    desc = site.get_item_desc(item)
    link = site.get_item_link(item)
    img = site.get_item_image(item)
    price = site.get_item_price(item)
    unit = site.get_item_unit(item)
    sitename = site.name
    specs = get_specs(site, item, link)

    res_dict = {"Desc" : desc, "Link" : link, "Image" : img, "Price" : price, "Unit" : unit, "Sitename" : sitename, "Categories" : cats[1:], "Specs" : specs}
    
    # write_to_db(desc, link, img, price, unit, sitename, cats[1:], specs)

    res_dict["Desc"] = unidecode.unidecode(res_dict["Desc"])
    logger.info("Thread: " + str(site.thread) + " " + str(res_dict))



def get_specs(site, item, link):

    specs = None
    if(site.specs_on_same_page(item)):
        specs = site.get_item_specs(item)
    else:
        prev_url = site.browser.current_url
        site.follow_url(link)
        
        specs = site.get_item_specs()
        site.follow_url(prev_url)


    return specs

# TODO make seperate file for testing and one for errors

def test(site, link, func, arg):
    print("starting tester...")
    site.url = link

    if(type(arg) is not str):
        raise ValueError("Fourth argument must be a String")

    elif(arg.lower() == "browser"):
        print("starting browser...")
        site.browser = c.get_headless_selenium_browser()
        site.browser.get(link)
        print("running function...")
        res = func()
        
        if(type(res) == list and len(res) == 0):
            print("Empty List!")
        elif(type(res) == list):
            for val in res:
                print("----------------------------------------")
                print(val.text)
        else:
            print("----------------------------------------")
            print(res)
            print("----------------------------------------")

    elif(arg.lower() == "cat"):
        print("starting browser...")
        site.browser = c.get_headless_selenium_browser()
        site.browser.get(link)

        if(not site.is_cat_page()):
            raise ValueError("Second argument must be the link for the page of categories")
        cats = site.get_cats()
        print("running function...")
        for cat in cats:
            print("----------------------------------------")
            print(func(cat))

    elif(arg.lower() == "item"):
        print("starting browser...")
        site.browser = c.get_headless_selenium_browser()
        site.browser.get(link)

        if(not site.is_prod_page()):
            raise ValueError("Second argument must be the link for the page of products")

        print("running function...")
        for i in range(len(site.get_prods())):
            items = site.get_prods()
            print("----------------------------------------")
            print(func(items[i]))

    else:
        raise ValueError("Fourth argument not recognized, must be either \"browser\", \"cat\", or \"item\"")



def main():
    if(len(sys.argv) < 3 or len(sys.argv) > 3):
        print("To crawl site:")
        print("    Usage: python GeneralizedCrawler.py crawl 'crawler name'")
        print("To test site:")
        print("    Usage: python GeneralizedCrawler.py test 'crawler name'")
        exit()

    crawler_factory = af.AbstractCrawlerFactory.get_crawler_factory(sys.argv[2])

    if(sys.argv[1] == "crawl"):
        crawl_site(crawler_factory)
    elif(sys.argv[1] == "test"):
        site = crawler_factory.get_crawler()
        test(site, "https://www.kele.com/access-control/1510-series.aspx", site.get_item_price, "item")



class UknownPage(ValueError):

    def __init__(self):
        ValueError("Unable to crawl page")



if(__name__ == "__main__"):
	main()
