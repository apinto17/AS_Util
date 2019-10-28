from abc import ABC, abstractmethod

import grainger_cat_crawler as gcc
import crawler as c
import errors as e
import time
import re

# import mysql
# import mysql.connector
# import sshtunnel



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
    	e.NO_SITE_FOUND(site.url, tb)
    	return

    DFS_on_categories(site, browser, cats)



# depth first search starting on the first category
def DFS_on_categories(site, browser, cats):

    print("top")
    print(browser.current_url)

    if(site.is_prod_page(browser)):
        print("On Product Page")

    elif(site.is_cat_page(browser)):

        for i in range(len(site.get_cats(browser))):

            c.sleep_counter(c.SLEEP_TIME)

            # update list
            cat_list = site.get_cats(browser)
            print("bottom")
            print(browser.current_url)
            print(i)
            cats += "|" + site.get_cat_name(cat_list[i])
            print(site.get_cat_name(cat_list[i]))

            # click on category
            prev_url = browser.current_url
            click_on_page(browser, site, cat_list[i])

            # depth first search on category
            DFS_on_categories(site, browser, cats)

            # restore previous browser
            site.url = prev_url
            browser.get(prev_url)

    else:
        print("Not scrapping page")
        e.UNKNOWN_PAGE(browser.current_url)
        return


def click_on_page(browser, site, page):

    browser.execute_script("return arguments[0].scrollIntoView();", page)
    time.sleep(1)
    page.click()
    site.url = browser.current_url



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
    grainger_cat = gcc.grainger_cat_crawler("https://www.grainger.com/category?analytics=nav", "Grainger", "https://www.grainger.com/")
    crawl_site(grainger_cat)


class Site(ABC):

    # url is the url you want to start at as a string
    # name is the display name of the site as a string
    # header is the beginning of the site url as a string ("www.abc.com/") can be blank if website
    #       uses absolute links
    def __init__(self, url, name, header):
        self.url = url
        self.name = name
        self.header = header
        super().__init__()

    def is_cat_page(self, browser):
        try:
        	res = self.get_cats(browser)
        	if(res != None and len(res) > 0):
        		return True
        	else:
        		return False
        except:
        	return False

    def is_prod_page(self, browser):
        try:
        	res = self.get_prods(browser)
        	if(res != None and len(res) > 0):
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
    # return a list of products as browser objects
    @abstractmethod
    def get_prods(self, browser):
    	pass



if(__name__ == "__main__"):
	main()
