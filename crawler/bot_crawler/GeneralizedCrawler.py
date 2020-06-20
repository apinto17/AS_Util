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


def crawl_site(crawler_factory):
    site = crawler_factory.get_crawler()
    # make folder
    if(not os.path.isdir(site.name)):
        os.mkdir(site.name)

    home_url = site.url

    # get terms of service and robots.txt
    site.browser = c.get_headless_selenium_browser()
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
    if(cats == ""):
        init(site, start, end)

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

    if(site.is_prod_page()):
        scrape_page(site, cats)

    if(not site.is_prod_page() and not site.is_cat_page()):
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
    logging.info("Thread: " + str(site.thread) + " start: " + str(start) + " end: " + str(end))


def log_exit(counter, prim_cat_list, site):
    if(counter == len(prim_cat_list)):
        logging.info("Thread " + str(site.thread) + " finished")
    else:
        logging.error("Thread " + str(site.thread) + " incomplete, missed " + str((len(prim_cat_list) - counter)) + " categories")



def click_on_page(site, page):
    try:
        page = page.find_element_by_css_selector("a")
    except:
        pass 
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
    crawled_items = []
    for i in range(len(site.get_prods())):
        time.sleep(c.SLEEP_TIME)
        prod_list = site.get_prods()

        try:
            item = (cats, site.get_item_desc(prod_list[i]))
            if(item not in crawled_items):
                get_item_info(site, prod_list[i], cats)
                crawled_items.append(item)
        except:
            logging.error("Thread: " + str(site.thread) + " COULDN'T SCRAPE ITEM NUMBER " + str(item_num) + " URL " + site.url + " Categories:   " + cats, exc_info=True)




def get_item_info(site, item, cats):
    desc = site.get_item_desc(item)
    link = site.get_item_link(item)
    img = site.get_item_image(item)
    price = site.get_item_price(item)
    unit = site.get_item_unit(item)
    sitename = site.name
    specs = get_specs(site, item)

    res_dict = {"Desc" : desc, "Link" : link, "Image" : img, "Price" : price, "Unit" : unit, "Sitename" : sitename, "Categories" : cats[1:], "Specs" : specs}

    # write_to_db(desc, link, img, price, unit, sitename, cats[1:], specs)

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

# TODO make seperate file for testing and one for errors

def test(site, link, func, arg):

    site.url = link

    if(type(arg) is not str):
        raise ValueError("Fourth argument must be a String")

    elif(arg.lower() == "browser"):
        site.browser = c.get_headless_selenium_browser()
        site.browser.get(link)

        res = func()

        if(type(res) == list):
            for val in res:
                print("----------------------------------------")
                print(val.text)
        else:
            print("----------------------------------------")
            print(res)
            print("----------------------------------------")

    elif(arg.lower() == "cat"):
        site.browser = c.get_headless_selenium_browser()
        site.browser.get(link)

        if(not site.is_cat_page()):
            raise ValueError("Second argument must be the link for the page of categories")
        cats = site.get_cats()
        for cat in cats:
            print("----------------------------------------")
            print(func(cat))

    elif(arg.lower() == "item"):
        site.browser = c.get_headless_selenium_browser()
        site.browser.get(link)

        if(not site.is_prod_page()):
            raise ValueError("Second argument must be the link for the page of products")

        for i in range(len(site.get_prods())):
            items = site.get_prods()
            print("----------------------------------------")
            print(func(items[i]))

    else:
        raise ValueError("Fourth argument not recognized, must be either \"browser\", \"cat\", or \"item\"")



def main():
    if(len(sys.argv) < 2 or len(sys.argv) > 2):
        print("Usage: python GeneralizedCrawler.py 'crawler name'")
        exit()
    crawler_factory = af.AbstractCrawlerFactory.get_crawler_factory(sys.argv[1])
    crawl_site(crawler_factory)
    #site = crawler_factory.get_crawler()
    #test(site, "https://www.vallen.com/categories", site.get_cat_name, "cat")



class UknownPage(ValueError):

    def __init__(self):
        ValueError("Unable to crawl page")



if(__name__ == "__main__"):
	main()
