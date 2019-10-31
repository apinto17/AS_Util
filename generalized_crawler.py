from abc import ABC, abstractmethod

import rs_hughes_crawler as rsh
import crawler as c
import errors as e
import time
import re
import multiprocessing as mp

import mysql
import mysql.connector
import sshtunnel



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


def crawl_site(site, server, cats=""):

    c.sleep_counter(c.SLEEP_TIME)

    browser = c.get_headless_selenium_browser()
    try:
    	browser.get(site.url)
    except:
    	e.NO_SITE_FOUND(site.url, tb)
    	return

    DFS_on_categories(site, browser, cats, server)



# depth first search starting on the first category
def DFS_on_categories(site, browser, cats, server):

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
            DFS_on_categories(site, browser, cats, server)

            # restory previous browser
            site.url = prev_url
            browser.get(prev_url)

    elif(site.is_prod_page(browser)):
        print("Scrapping page")
        print(browser.current_url)
        scrape_page(site, browser, cats, server)

    else:
        print("Not scrapping page")
        e.UNKNOWN_PAGE(browser.current_url)
        return


def click_on_page(browser, site, page):

    browser.execute_script("return arguments[0].scrollIntoView();", page)
    time.sleep(1)
    page.click()
    site.url = browser.current_url


# go through every page and scrape info
def scrape_page(site, browser, cats, server):

    # scrape show all page if it exits
    if(site.has_show_all_page(browser)):
        c.sleep_counter(c.SLEEP_TIME)
        site.get_show_all_page(browser).click()
        get_prods_info(site, browser, cats, server)

    # else if there is a page list, scape pages
    elif(site.has_page_list(browser)):

        c.sleep_counter(c.SLEEP_TIME)
        # scrape products on the first page
        get_prods_info(site, browser, cats, server)

        # scrape products on subsequent pages
        for i in range(len(site.get_prod_pages(browser))):

            c.sleep_counter(c.SLEEP_TIME)

            page_list = site.get_prod_pages(browser)

            prev_url = browser.current_url
            click_on_page(browser, site, page_list[i])

            get_prods_info(site, browser, cats, server)

            site.url = prev_url
            browser.get(prev_url)

    # else if the site only has a page turner
    elif(site.has_page_turner(browser)):
        c.sleep_counter(c.SLEEP_TIME)
        # scrape products on the first page
        get_prods_info(site, browser, cats, server)

        # scrape subsequent pages
        while(True):
            c.sleep_counter(c.SLEEP_TIME)

            click_on_page(browser, site, site.get_next_page(browser))

            get_prods_info(site, browser, cats, server)

            if(not site.has_page_turner(browser)):
                break

    # else scrape the page
    else:
        c.sleep_counter(c.SLEEP_TIME)
        get_prods_info(site, browser, cats)


def get_prods_info(site, browser, cats, server):
    for i in range(len(site.get_prods(browser))):
        prod_list = site.get_prods(browser)
        get_item_info(site, browser, prod_list[i], cats, server)



def get_item_info(site, browser, item, cats, server):
    desc = site.get_item_desc(item)
    link = site.header + site.get_item_link(item)
    img = site.get_item_image(item)
    price = site.get_item_price(item)
    unit = site.get_item_unit(item)
    sitename = site.name
    specs = get_specs(site, item, browser)


    print("\n\n--------------------------------------------------------")
    print("DESC")
    print(desc)
    print("LINK")
    print(link)
    print("IMAGE")
    print(img)
    print("PRICE")
    print(price)
    print("UNIT")
    print(unit)
    print("SITENAME")
    print(sitename)
    print("CATEGORIES")
    print(cats[1:])
    print("SPECS")
    print(specs)

    server.write_to_db(desc, link, img, price, unit, sitename, cats[1:], specs)


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
    server = Server()
    server.connect()
    rshughes = rsh.rs_hughes_crawler("https://www.rshughes.com/c/pneumatic-and-electric-power-tools/680/", "rshughes.com", "")
    crawl_site(rshughes, server)
    del server


class Server:

    server = None
    connection = None
    mycursor = None

    def __init__(self):
        sshtunnel.SSH_TIMEOUT = 350.0
        sshtunnel.TUNNEL_TIMEOUT = 350.0

        self.server = sshtunnel.SSHTunnelForwarder('ssh.pythonanywhere.com',
            			  ssh_username='iclam19',
            			  ssh_password='@astest@1234',
            			  remote_bind_address=('iclam19.mysql.pythonanywhere-services.com'
            			  , 3306))
        self.server.start()


    def write_to_db(self, desc, link, img, price, unit, sitename, cats, specs):
        txntime_cd = datetime.datetime.utcnow()
        sql = \
          'INSERT INTO  ft_crawled_data (site_name,category,item_description,price,url,image_source,txntime,unit,specs) VALUES (%s, %s,%s, %s,%s,%s,%s,%s,%s)'
        val = (str(sitename), str(cats), str(desc), str(price), str(link),str(img),str(txntime_cd),str(unit), str(specs))
        self.mycursor.execute(sql, val)
        self.connection.commit()


    def __del__(self):
        self.connection.close()
        self.server.stop()


    def connect(self):

        try:

            self.connection = mysql.connector.connect(user='iclam19',
                password='astest1234', host='127.0.0.1',
                port=self.server.local_bind_port,
                database='iclam19$AssembledSupply')

            if(self.connection.is_connected()):
                self.mycursor = self.connection.cursor()
            else:
                print("Did not connect")
        except Error as e:
            print(e)


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
