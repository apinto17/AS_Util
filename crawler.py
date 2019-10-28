import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

import copy

import datetime
import sqlite3

import mysql
import mysql.connector
import sshtunnel


import random
import math
import time
import sys
import re

# from .import errors as e
import errors as e

SLEEP_TIME = 5




# SCRAPE ME WHAT YOU'VE GOT!!
# ____________  ________
#             \/
#         ___
#     . -^   `--,
#    /# =========`-_
#   /# (--====___====\
#  /#   .- --.  . --.|
# /##   |  * ) (   * ),
# |##   \    /\ \   / |
# |###   ---   \ ---  |
# |####      ___)    #|
# |######           ##|
#  \##### ---------- /
#   \####           (
#    `\###          |
#      \###         |
#       \##        |
#        \###.    .)
#         `======/

data = None

proxy = None
user_agent = None


def get_records(items):

  # put_into_database()
    # Crawlers In Development
  # get_rock_west_composites_items("https://www.rockwestcomposites.com/")

    #Functioning Crawlers
    #Production tool supply blocked out my internet provider
    # get_production_tool_supply_items("http://www.pts-tools.com/cgi/CGP2HOME")

  #Useful reference for recursive trap of automation direct
  # get_automation_direct_items("https://www.automationdirect.com/adc/shopping/catalog/hmi_(human_machine_interface)/c-more_touch_panels/c-more_touch_panels_ea7_series/c-more_ea7_series_touch_panels")

  #Actual url for crawling automation direct:
  # get_automation_direct_items("https://www.automationdirect.com/adc/Home/Home")

  # get_subcategories_recursive_blackhawk_industrial("https://www.bhid.com/CatSearch/4724/jobber-drills/238")

  #Run This One
  # get_blackhawk_industrial_items("https://www.bhid.com/")


  # get_blackhawk_industrial_items("https://www.bhid.com/CatSearch/1344/diamond-super-abrasives")

  # get_blackhawk_industrial_items("https://www.bhid.com//CatSearch/676/buffing-compound")
  # get_directools_items("https://www.directools.com/")
  # get_baleigh_industrial_items("https://www.baileigh.com/metalworking")
  # get_baleigh_industrial_items("https://www.baileigh.com/woodworking")

  # get_qc_industrial_items("https://www.qcsupply.com/commercial-industrial.html?product_list_limit=72")
  # get_qc_industrial_items("https://www.qcsupply.com/commercial-industrial.html?p=48&product_list_limit=72")


  # get_product_info_speedy_metals("http://www.speedymetals.com/pc-6470-8258-1-12-x-4-303-stainless-flat-28-long.aspx")
  # get_speedymetals_items("http://www.speedymetals.com/")

  # get_online_metals_items("https://www.onlinemetals.com/allmetals.cfm?all_metals=1")

  # get_fastener_superstore_items("https://www.fastenersuperstore.com/")

  # get_air_gas_items("http://www.airgas.com/category/viewAllCategories/")

  # get_air_gas_items("http://www.airgas.com/category/Safety-Products-Clothing-Flame-Resistant-Clothing/_/N-84o")

  # get_HSC_items("https://www.halted.com/commerce/misc/allproducts.jsp?czuid=1538261660904")

  # get_tanner_bolt_items(" https://www.tannerbolt.com/products/FASTENERS/SCREWS/SELF-DRILLING-SCREWS/SELF-DRILLING-SCREWS-STANDARD.aspx")
  # get_tanner_bolt_items(" https://www.tannerbolt.com/products/FASTENERS/SCREWS/SELF-DRILLING-SCREWS/SELF-DRILLING-SCREWS-STANDARD.aspx")
  # get_tanner_bolt_items("https://www.tannerbolt.com/products/SAFETY%20PRODUCTS/FALL-PROTECTION/DROP-PROTECTION/PROTO-TETHER-READY-TOOLS.aspx")

  # get_tanner_bolt_items("http://www.tannerbolt.com/?page=customer&file=customer/tabonu/b2bse/includes/shop.aspx")

  # get_hsc_electronics_items("https://www.halted.com/commerce/misc/allproducts.jsp?czuid=1538326408745")

  # get_RSHughes_items()
  # get_dillon_supply_items()
  # get_AWC_items()
  get_stellar_industrial_items("http://www.stellarindustrial.com/default.aspx?page=category")
    #Obsolete Crawlers Located in obsolete_crawlers.py


###Begin Development Crawlers Section:


def get_stellar_industrial_items(url, cats=""):

    sleep_counter(SLEEP_TIME)
    print(url)

    soup = headless_selenium_and_soup(url)
    if(soup == None):
        return e.NO_SITE_FOUND

    # if you're in a category page
    if(soup.find("div", {"class": "CategoryWrapper"}) != None):
        DFS_on_categories_stellar(soup, cats)

    # if you're in a product page
    elif(soup.find("div", {"class" : "Product"}) != None):
        scrape_page_stellar(soup, cats)


# go through every page and scrape info
def scrape_page_stellar(soup, cats):

    for page in soup.findAll("a", {"class", "ItemSearchResults_PageLinks"}):
        link = "http://www.stellarindustrial.com" + page['href']
        ssh_connection = get_ssh_connection()
        for item in soup.findAll("div", {"class" : "Product"}):
            get_stellar_industrial_info(item, cats, ssh_connection[0], ssh_connection[1])
        ssh_connection[0].close()
        sleep_counter(SLEEP_TIME)
        soup = headless_selenium_and_soup(link)

# depth first search starting on the first category
def DFS_on_categories_stellar(soup, cats):

    for cat in soup.findAll("div", {"class" : "CategoryWrapper"}):
        cat_name = cat.find("div", {"class" : "CategoryTitle"}).string
        if(cat_name == None):
            cat_name = cat.findAll("a", {"class" : "CatalogTopItems_CategoryLinks"})[1].string
        cat_name = cats + cat_name.strip(" \n\t")
        cat_link = cat.find("a", {"class" : "CategoryLink"})['href']
        get_stellar_industrial_items("http://www.stellarindustrial.com" + cat_link, cat_name + "|")


def get_stellar_industrial_info(item, cats, connection, mycursor):

    desc = ""
    if(item.find("div", {"class" : "ProductDesc"}) != None):
        desc = item.find("div", {"class" : "ProductDesc"}).a.p.string

    link = ""
    if(item.find("a", {"class" : "ItemDetailsLink"}) != None):
        link = "https://www.stellarindustrial.com/" + item.find("a", {"class" : "ItemDetailsLink"})['href']

    image = ""
    if(item.find("img", {"class" : "ItemSearchResults_Thumbnail_new"}) != None):
        image = item.find("img", {"class" : "ItemSearchResults_Thumbnail_new"})['src']

    print(desc + "\n\n")
    print(link+ "\n\n")
    print(image + "\n\n")


def get_ssh_connection():

    sshtunnel.SSH_TIMEOUT = 350.0
    sshtunnel.TUNNEL_TIMEOUT = 350.0

    print("Getting Connection. . . ")

    with sshtunnel.SSHTunnelForwarder('ssh.pythonanywhere.com',
                      ssh_username='iclam19',
                      ssh_password='@astest@1234',
                      remote_bind_address=('iclam19.mysql.pythonanywhere-services.com'
                      , 3306)) as tunnel:
      connection = mysql.connector.connect(user='iclam19',
        password='astest1234', host='127.0.0.1',
        port=tunnel.local_bind_port,
        database='iclam19$AssembledSupply')

      mycursor = connection.cursor()

      print("Got Connection")

      return (connection, mycursor)




def get_tanner_bolt_items(url, cat=""):

  sleep_counter(SLEEP_TIME)

  soup = None
  soup = headless_selenium_and_soup(url)

  delimiters = ["/products/BY-BRAND.aspx", "/products/BY-INDUSTRY.aspx", "/products/SPECIALS.aspx"]


  if(soup == None):
    print("You dun goofed")

  # going through categories: Note, this segment commented out to resume crawling midway...
  elif(soup.find("div", {"class" : ["HomeCat", "CategoryWrapper"]}) != None):

    for cat in soup.findAll("div", {"class" : ["HomeCat", "CategoryWrapper"]}):
      if(cat.a['href'] not in delimiters):
        cat_name = ""
        if(cat.find("div", {"class" : "CategoryTitle"}) != None):
          cat_name = cat.find("div", {"class" : "CategoryTitle"}).string
        else:
          cat_name = cat.find("div", {"class" : "catname"}).p.string
        get_tanner_bolt_items("http://www.tannerbolt.com" + cat.a['href'], cat_name)



  # finding show all page and scrapping items
  elif(soup.find("div", {"class" : "Product"})):

    #Finding the category tree for the page, then writing it to the DB.
    #This function falls under the "if product found" logic because
    #it should only happen on pages where items exist, as this is the
    #bottom level of the category tree.
    delimiter =">>"
    category_div = soup.find("div", {"class" : "BreadCrumbcategorytree_activepage"})
    category_tree = get_category_tree(category_div, delimiter)
    print(category_tree)

    #Double Check this line for category stuff
    cat = category_tree
    # for category in category_name_bottom:
      # print(category)

    # category_parents = category_div.findAll("a")
    # del category_parents[0]
    # for parent in category_parents:
    #   print(parent.text)


    print("That's all the category parents we have")
    # time.sleep(10000)
    pages = soup.find("td", {"id" : "ItemSearchResults_PaginationLinksTD"})

    # if there is more than one page, get show all page
    show_all_page = None
    if(pages != None):

      # find show all page and scrape items
      page_list = pages.findAll("option")

      if(page_list != []):
        show_all_page = page_list[9]['value']
        code = get_secure_connection(show_all_page)
        soup = BeautifulSoup(code.text, "html.parser")



        sshtunnel.SSH_TIMEOUT = 550.0
        sshtunnel.TUNNEL_TIMEOUT = 550.0

        with sshtunnel.SSHTunnelForwarder('ssh.pythonanywhere.com',
                          ssh_username='iclam19',
                          ssh_password='@astest@1234',
                          remote_bind_address=('iclam19.mysql.pythonanywhere-services.com'
                          , 3306)) as tunnel:
          connection = mysql.connector.connect(user='iclam19',
            password='astest1234', host='127.0.0.1',
            port=tunnel.local_bind_port,
            database='iclam19$AssembledSupply')

          mycursor = connection.cursor()


          for product in soup.findAll("div", {"class" : "Product"}):
            get_product_info_tanner(product, cat, connection, mycursor)
          connection.close()

      # if you couldnt find the show all page, go through every page and scrape
      else:
        for page in pages.findAll("a"):

          link = "https://www.tannerbolt.com/" + page['href']
          sleep_counter(4)

          code = get_secure_connection(link)
          soup = BeautifulSoup(code.text, "html.parser")


          sshtunnel.SSH_TIMEOUT = 550.0
          sshtunnel.TUNNEL_TIMEOUT = 550.0

          with sshtunnel.SSHTunnelForwarder('ssh.pythonanywhere.com',
                            ssh_username='iclam19',
                            ssh_password='@astest@1234',
                            remote_bind_address=('iclam19.mysql.pythonanywhere-services.com'
                            , 3306)) as tunnel:
            connection = mysql.connector.connect(user='iclam19',
              password='astest1234', host='127.0.0.1',
              port=tunnel.local_bind_port,
              database='iclam19$AssembledSupply')

            mycursor = connection.cursor()

            for product in soup.findAll("div", {"class" : "Product"}):
              get_product_info_tanner(product, cat, connection, mycursor)
            connection.close()



def get_product_info_tanner(product, cat, connection, mycursor):
  print("Desc")
  desc = product.p.string
  if desc != None:
    print(desc + "\n")
    desc = product.p.string

    print("Link")
    print("https://www.tannerbolt.com/" + product.a['href'] + "\n")
    link ="https://www.tannerbolt.com/"+ product.a['href']

    print("Img")
    print(product.img['src'] + "\n")
    img =product.img['src']


    delimiter = "https://www.tannerbolt.com/"
    length = len(delimiter)
    img_start = (img[:length])
    if img_start != delimiter:
      img = "https://www.tannerbolt.com/" + img
      print("I caught the image thingamabobber!!")
      print(img)


    print("Price")
    try:
      print(product.find("span", {"class" : "Price"}).a.string + "\n")
      price = product.find("span", {"class" : "Price"}).a.text
    except:
      print(product.find("span", {"class" : "Price"}).text + "\n")
      price = product.find("span", {"class" : "Price"}).text

    print("Price Unit")
    print(product.find("span", {"class" : "UnitSize"}).string + "\n")
    unit = product.find("span", {"class" : "UnitSize"}).string

    print("Category")
    # cat = soup.find("div", {"class" : "BreadCrumbcategorytree_activepage"})
    # cat_list = cat_container.findAll("a")
    # cat = cat_list[len(cat_list) - 1].string
    print(cat)

    print("Sitename")
    print("Tanner Bolt")
    sitename = "Tanner Bolt"

    print("\n--------------------------------------------\n")
    put_into_mysql_database(desc, link, img, price, sitename, cat, mycursor, connection)
    # time.sleep(1000)
    # put_into_database(desc, link, img, price, sitename, cat, unit)
    # (desc, link, img, price, sitename, category, unit="")


def get_rock_west_composites_items(url, cat_name=""):

  sleep_counter(SLEEP_TIME)
  soup = None

  browser = get_selenium_browser()
  browser.get(url)
  code = browser.page_source
  # print(code)
  soup = BeautifulSoup(code, "html.parser")

  # print(soup)
  # nav =
  print("Crawling for Rocks. Using the Rockwest crawler")
  if(soup == None):
    print("WHHHHHHYYYYYYY!!!")
    return None

  elif(soup.find("nav", {"id" : "nav"}) != None):
    navigation_bar = soup.find("nav", {"id" : "nav"})
    print("Im in the navigation bar")
    # print(navigation_bar)
    nav_categories = navigation_bar.findAll("li", {"class" : ["level0 nav-1 category first parent", "level0 nav-2 category parent", "level0 nav-3 category parent","level0 nav-4 category parent","level0 nav-5 category parent","level0 nav-6 category parent"]})
    nav_length = len(nav_categories)
    print(nav_categories)
    print(nav_length)
    # nav_length = 1


    #Hard Coding this in to make it easier to run down only one category for now!
    # nav_length = 1

    for i in range(nav_length):
      print("Now Scraping Navigation Header Category...")
      category = nav_categories[i]
      category_link = category.a['href']
      print(category_link)

      print("Initiating a new browser...")
      # browser = get_selenium_browser()
      # browser.get(category_link)
      # code = browser.page_source
      # # print(code)
      # soup = BeautifulSoup(code, "html.parser")


      code = get_secure_connection(category_link)
      soup = BeautifulSoup(code.text, "html.parser")



      if(soup.find("tbody", {"id" : "products-table-body"}) != None):
        print("hooray I'm hungry for apples")

        #Note: Rock west has a really goofy edge case! It uses a table that's entirely populated with JS
        #And the JS function doesn't do anything until the user scrolls down to a certain point of the page
        #So the traditional page load sequence for acquiring JS populated data doesn't work.
        #In the context of developing the database for Rock West, this probably is not worthwhile. However,
        #if we are planning to pursue a selenium-based web-browser going forward, it's probably a good
        #time investment to learn how to do it now...
        product_table = soup.findAll("tbody", {"id" : "products-table-body"})
        print(product_table)
        table_items = product_table.findAll("tr", {"class" : ["product simple even","product simple odd"]})
        print(table_items[1])


###End In-Development Crawlers


### Begin Functioning Crawlers. Ready to Crawl and Catalog Data, but need to comment out put_into_db functions


#The speedymetals crawler uses UrlLib to retrieve html, and beautifulsoup for scraping. The
#crawler does not use selenium. The subcategories crawler is recursive, as is the page turner.
#Normally a recursive page-turner is not ideal, however there are only 2-3 pages maximum which
#need to be turned, so running out of memory is not a huge issue.
def get_speedymetals_items(url):
  soup = None
  sleep_counter(SLEEP_TIME)
  code = get_secure_connection(url)
  soup = BeautifulSoup(code.text, "html.parser")

  if(soup == None):
    print("WHHHHHHYYYYYYY!!!")
    return None

  #Find the navigator menu
  menu = soup.find("div", {"id" : "menudiv"})
  dropdown_list = menu.findAll("li")
  #Delete the last item in the nav, as it is dedicated to fire-sale items
  del dropdown_list[-1]
  #Open up each page in the nav
  for item in dropdown_list:
    sub_list = item.div.findAll("a")
    for sub_item in sub_list:
      href = sub_item['href']
      link = url+href
      print(link)
      browse_subcategories_speedymetals(link)


def browse_subcategories_speedymetals(url):
  speedymetals_url = "http://www.speedymetals.com/"
  sleep_counter(4)
  soup = None
  code = get_secure_connection(url)
  soup = BeautifulSoup(code.text, "html.parser")

  #Look for a list of product types
  product_table = soup.find("div", {"class" : "ProductTable"})
  #If there's no product table then that means the crawler must go down a level
  if product_table == None:
    print("There's no Product Table")
    #Look for categories to go down
    category_container = soup.find("div", {"class" : "ShapeContainer"})
    #Open each of the category pages in the same function
    if category_container != None:
      category_list = category_container.findAll("div")
      for category in category_list:
        href = category.a['href']
        link = speedymetals_url + href
        browse_subcategories_speedymetals(link)

    else:
      print("Empty category")
      # time.sleep(10000)

  #If there is a product table then go looking for items in it
  else:
    print("Found product table")
    go_to_product_page_speedymetals(url)

def go_to_product_page_speedymetals(url):
  print("On a Page With Items")
  speedymetals_url = "http://www.speedymetals.com/"

  print(url)
  sleep_counter(4)
  soup = None
  code = get_secure_connection(url)
  soup = BeautifulSoup(code.text, "html.parser")

  product_table = soup.find("div", {"class" : "ProductTable"})
  product_list = product_table.findAll("a", {"class" : "toProductClick"})
  for product in product_list:
    href = product['href']
    link = speedymetals_url + href
    get_product_info_speedy_metals(link)

  #Turn pages if necessary
  page_turn_container = soup.find("div", {"class" : "pagenum"})
  page_turn_link_list = page_turn_container.findAll("a")
  if page_turn_link_list != None and page_turn_link_list != []:
    print("Here's the page turn list")
    print(page_turn_link_list)
    print("That was the page turn list")
    page_pointer = page_turn_link_list[-1]
    page_pointer_img = page_pointer.img

    #Keep running the function looking for items until there are no more pages
    if page_pointer_img != None:
      href = page_pointer['href']
      link = speedymetals_url + href
      go_to_product_page_speedymetals(link)
    else:
      print("Last page in the list")



def get_product_info_speedy_metals(url):
  print("On product page")
  print(url)
  sleep_counter(4)
  speedymetals_url = "http://www.speedymetals.com/"
  sitename = "Speedy Metals"

  soup = None
  code = get_secure_connection(url)
  soup = BeautifulSoup(code.text, "html.parser")

  delimiter = "→"
  category_tree_container = soup.find("div", {"class" : "breadcrumbnav"})
  category_tree = get_category_tree(category_tree_container,delimiter)
  print(category_tree)
  # time.sleep(1000)
  cat = category_tree

  #Note: The image, category, and part of the item description are shared between
  #all items on the same page.
  #Product Name
  product_name_container = soup.find("div", {"class" : "ProductNameText"})
  #Some pages don't have proper product names or info.
  if product_name_container != None:

    sshtunnel.SSH_TIMEOUT = 550.0
    sshtunnel.TUNNEL_TIMEOUT = 550.0

    with sshtunnel.SSHTunnelForwarder('ssh.pythonanywhere.com',
                      ssh_username='iclam19',
                      ssh_password='@astest@1234',
                      remote_bind_address=('iclam19.mysql.pythonanywhere-services.com'
                      , 3306)) as tunnel:
      connection = mysql.connector.connect(user='iclam19',
        password='astest1234', host='127.0.0.1',
        port=tunnel.local_bind_port,
        database='iclam19$AssembledSupply')

      mycursor = connection.cursor()



      product_name = product_name_container.h1.text
      # print(product_name)

      #Image
      image_container = soup.find("div", {"class" : "ProductImage"})
      image = image_container.div.img['src']
      image_link = speedymetals_url+image
      # print(image_link)
      #Category
      category_container = soup.find("div", {"class" : "breadcrumbnav"})
      categories = category_container.findAll("a", {"class" : "SectionTitleText"})
      category = ""
      for category_link in categories:
        category_text = category_link.text
        category = category + category_text + " "
      category.strip()
      # print(category)
      # time.sleep(1000)

      #Find the individual items
      row_list = soup.findAll("div", {"class" : "ProductVariantRowInfo"})
      for row in row_list:
        # print(row)
        length = row.find("div", {"class" : "ProductVariantRowCellName"}).text
        #Add the size to the shared product name description
        description = product_name + " - " + length
        print(description)
        price = row.find("div", {"class" : "ProductVariantRowCellPrice"}).div.div.text
        print(price)

        put_into_mysql_database(description, url, image_link, price, sitename, cat, mycursor, connection)
        # time.sleep(1000)
      connection.close()
        # put_into_database(description, url, image_link, price, sitename, category)


#The Production Tool Supply uses a primarily selenium-driven
#crawler. There are almost no links available to browse categories
#within production tool supply, so selenium "click" functions are used
#for most of the navigation. Additionally, the url which is reached after some
#click operations leads to a "not found" result when typed back into the seach bar
#manually, or when opened by a new browser. This is likely because the links
#have mostly been replaced with js form elements, so simply returning to the url
#doesn't work because there is missing form information which is needed to intiailize
#the webpage. Finally, "shift-click" does not open a new page, but instead navigates
#from the existing browser.
#This crawler uses a click-based recursive page turner, and a non-recursive function
#to browse deeper within subcategories. The subcategories have different depths, which
#would typically favor a while loop or recursive function, however multiple browser clicks are
#needed just to get back to the page the browser is operating at, because the url
#cannot be used to reopen the current page. "production_tool_supply_category_searcher" handles
#this subcategory crawling, although it is a bit crude, and we may want to rewrite it.
def get_production_tool_supply_items(url, cat_name=""):

  sleep_counter(SLEEP_TIME)
  soup = None
  browser = get_selenium_browser()
  browser.get(url)
  code = browser.page_source
  soup = BeautifulSoup(code, "html.parser")


  print("Crawling for Production Tools. Using the Production tool supply crawler")
  if(soup == None):
    print("There is no soup on the homepage even though there should be")
    return None

  nav = soup.find("div", {"class" : "sidebar1"})
  time.sleep(4)
  if(nav != None):
    print("I found a navigator heading")

    nav_list_container = nav.find("ul", {"class" : "sub-nav"})
    nav_items = nav_list_container.findAll("li")
    #The first item in nav_items is not a category link, so delete it
    del nav_items[0]
    i = 0
    browser.quit()
    for item in nav_items:
      #First, create a new browser
      secondary_browser = get_selenium_browser()
      secondary_browser.get(url)

      #Second, create a list of nav_items
      nav_list_elements = secondary_browser.find_elements_by_class_name("sub-nav")
      nav_list_element = nav_list_elements[0]
      print(nav_list_element)
      navigator_list = nav_list_element.find_elements_by_tag_name('li')
      #Delete the first item in the list again, as it's not a category
      del navigator_list[0]
      nav_element = navigator_list[i]
      nav_element.click()
      time.sleep(3)
      i = i +1
      production_tool_supply_category_searcher(secondary_browser)

  else:
    print("Something went wrong in the homepage")



def production_tool_supply_category_searcher(browser):
  code = browser.page_source
  soup = BeautifulSoup(code, "html.parser")
  url = browser.current_url

  #First, the searcher determines if there are any item containers
  prodList = soup.find("div", {"class" : "prodList"})
  if prodList == None:
    #If the searcher doesn't find items, it looks for a product table
    product_table = soup.find("div", {"id" : "product-tableC"})
    # print(product_table)
    #If it finds one, it creates a list from said table
    product_list = product_table.findAll("div", {"class" : "prodListContainer"})
    i = 0
    # browser.quit()

    #It then goes through all the categories in the list
    for product in product_list:
      #For each one, it creates a new browser, then creates a sublist.
      print(product)
      time.sleep(4)

      # #First, create a new browser
      secondary_browser = get_selenium_browser()
      secondary_browser.get(url)
      # time.sleep(5)

      # # Second, create a list of nav_items
      nav_list_element = secondary_browser.find_element_by_id("product-tableC")
      # print(nav_list_element)
      navigator_list = nav_list_element.find_elements_by_class_name("prodListContainer")

      nav_element = navigator_list[i]
      nav_element.click()
      time.sleep(3)

      #Get Subcategories
      #Get New soup
      code = secondary_browser.page_source
      soup = BeautifulSoup(code, "html.parser")
      #Find subcategories with soup

      #It then looks for another product table so it can go a layer deeper
      sub_product_table = soup.find("div", {"id" : "product-tableC"})
      if sub_product_table != None:

        #If it finds a table, then it creates a list from the table
        sub_product_list = sub_product_table.findAll("div", {"class" : "prodListContainer"})
        #Define J
        j = 0
        #And it goes again
        for sub_product in sub_product_list:
        #Make a browser
          tertiary_browser = get_selenium_browser()
          tertiary_browser.get(url)
          # time.sleep(5)
          # print(len(sub_product_list))
          # time.sleep(5)


          #Go into the subcategory we're currently in.
          #This is implemented because when it launches a browser,
          #The function actually has to start a layer "back" from
          #Where it has currently reached. (URL inputs stop working
          #past a certain level of browsing. Thanks PTS)

          nav_list_element = tertiary_browser.find_element_by_id("product-tableC")
          # print(nav_list_element)
          navigator_list = nav_list_element.find_elements_by_class_name("prodListContainer")
          nav_element = navigator_list[i]
          nav_element.click()
          time.sleep(3)

          #Go a level deeper...
          nav_list_element = tertiary_browser.find_element_by_id("product-tableC")
          # print(nav_list_element)
          navigator_list = nav_list_element.find_elements_by_class_name("prodListContainer")
          nav_element = navigator_list[j]
          nav_element.click()
          time.sleep(3)

          #Reset soup so that it's based on the current browser location
          code = tertiary_browser.page_source
          soup = BeautifulSoup(code, "html.parser")

          #Look for another product table
          sub_sub_product_table = soup.find("div", {"id" : "product-tableC"})
          print("Sub product stuff")
          # time.sleep(5)
          if sub_sub_product_table != None:
            #If it finds one, create a list of the items
            sub_sub_product_list = sub_sub_product_table.findAll("div", {"class" : "prodListContainer"})

            #Define k for innermost loop
            k = 0
            print("Looking for the products")
            time.sleep(4)
            #For subcat in subcats
            for sub_sub_product in sub_sub_product_list:
              print("Pickles")

              #Make a browser
              quartiary_browser = get_selenium_browser()
              quartiary_browser.get(url)
              # print(len(sub_product_list))
              time.sleep(3)

              #Same as in previous loop.
              nav_list_element = quartiary_browser.find_element_by_id("product-tableC")
              # print(nav_list_element)
              navigator_list = nav_list_element.find_elements_by_class_name("prodListContainer")
              nav_element = navigator_list[i]
              nav_element.click()
              time.sleep(3)

              #Same as in previous loop.
              nav_list_element = quartiary_browser.find_element_by_id("product-tableC")
              # print(nav_list_element)
              navigator_list = nav_list_element.find_elements_by_class_name("prodListContainer")
              nav_element = navigator_list[j]
              nav_element.click()
              time.sleep(3)

              #Same as in previous loop, just one level deeper
              nav_list_element = quartiary_browser.find_element_by_id("product-tableC")
              # print(nav_list_element)
              navigator_list = nav_list_element.find_elements_by_class_name("prodListContainer")
              nav_element = navigator_list[k]
              nav_element.click()
              time.sleep(3)

              #Reset soup again so that it's based on the current browser location
              code = quartiary_browser.page_source
              soup = BeautifulSoup(code, "html.parser")

              #Look for another product table
              sub_sub_sub_product_table = soup.find("div", {"id" : "product-tableC"})
              print("Sub product stuff")
              # time.sleep(3)
              if sub_sub_sub_product_table != None:
                print("How the heck does it actually go deeper")
              else:
                print("We're the fourth level deep and we better have some items")
                item_page_searcher_production_tool_supply(quartiary_browser)
                # time.sleep(5)
              #Increment for innermost (k) loop
              k = k+1
          else:
            # time.sleep(5)
            item_page_searcher_production_tool_supply(tertiary_browser)
            print("Third level deep and there's items. This is where we call the get product info function")
            # time.sleep()
          #Increment j for loop
          j = j+1
      else:
        print("Pickles")
      i = i +1
  else:
    print("On an item page")

def item_page_searcher_production_tool_supply(browser):
  print("I am on an item page")
  results_per_page_element = browser.find_element_by_name("SIPERPAGE")
  results_per_page_element.click()

  time.sleep(1)

  number_per_page_list = results_per_page_element.find_elements_by_tag_name("option")
  forty_eight_per_page = number_per_page_list[2]
  forty_eight_per_page.click()
  # time.sleep(1)

  item_page_recursive_crawler_production_tool_supply(browser)

def item_page_recursive_crawler_production_tool_supply(browser):
  print("On the recursive page turner")
  time.sleep(3)
  pages_elements = browser.find_elements_by_class_name("pager")

  code = browser.page_source
  soup = BeautifulSoup(code, "html.parser")

  #Get Item info here...
  get_production_tool_supply_product_info(soup)

  if pages_elements == []:
    print("No Page elements")
    browser.quit()
  else:
    pages_element = pages_elements[0]
    pages_soup = soup.find("div", {"class" : "pager"})
    pages = pages_soup.find("li", {"class" : "next off"})
    if pages != None:
      print("Its not a nonetype")
      print(pages)
      # time.sleep(5)
      browser.quit()
      return
    else:
      print("It's a nonetype")
      print(pages)

      next_page_list = pages_element.find_elements_by_class_name("next")
      next_page = next_page_list[0]
      next_page.click()
      item_page_recursive_crawler_production_tool_supply(browser)
  browser.quit()

def get_production_tool_supply_product_info(soup):
  product_list_container = soup.find("div", {"class" : "prodList"})
  print(product_list_container)
  product_list = product_list_container.findAll("div", {"class" : "prodListContainer list "})
  for item in product_list:
    print("Writing To Database...")
    information_container = item.find("div", {"class" : "prodListInfoContainer"})
    print("DESCRIPTION")
    description_container = information_container.find("div", {"class" : "prodListDesc"})
    desc = description_container.span.text
    print(desc)
    print("\n\nLINK")
    product_number_container = information_container.find("div", {"class" : "prodListDtl"})
    product_number = product_number_container.div.span.text
    print(product_number)
    product_number_without_title = product_number.replace("Item:", "")
    product_number_bare = product_number_without_title.strip()
    print(product_number_bare)
    link = "http://www.pts-tools.com/cgi/CGP2SRIM?PMITEM=" + product_number_bare + "&PARTPG=CGP2LMXE&PAMENU=&PAHDID=000000196322221&PARDID=315096199659209"
    print(link)
    print("\n\nIMAGE")
    image_container = item.find("div", {"class" : "prodListImage"})
    img = image_container.img['src']
    print(img)
    print("\n\nPRICE")
    price_container = information_container.find("div", {"class" : "prodListPrice"})
    price = price_container.div.span.text
    print(price)
    print("\n\nSITENAME")
    sitename = "Production Tool Supply"
    print(sitename)
    print("\n\nCATEGORY")
    categories_container = soup.find("li", {"class" : "top-section"})
    categories_list = categories_container.findAll("li")
    last_category_index = len(categories_list) - 1
    last_category = categories_list[last_category_index]
    category = last_category.a.text

    print(category)
    print("STOP")
    # time.sleep(1)
    print("HAMMERTIME!")
    # time.sleep(10)
    put_into_database(desc, link, img, price, sitename, category)



#HSC Electronics Crawler
def get_hsc_electronics_items(url):
  print("url")
  print("\nOn HSC Electronics")
  soup = selenium_and_soup(url)

  #Defines the table
  table_container = soup.find("td", {"class" : "content"})
  table = table_container.table.tbody

  #Finds all the links in the master table
  links = table.findAll("a")

  #The first 6 links are not for categories, so they are removed
  for i in range(6):
    print(i)
    del links[0]
  # time.sleep(90)
  print(links[142])
  del links[150]
  del links[142]
  del links[126]
  del links[124]
  del links[122]
  del links[121]
  del links[120]
  del links[119]
  del links[118]
  del links[108]
  del links [103]
  del links[97]
  del links[90]
  del links[89]
  del links[81]
  del links[68]

  del links[50]
  time.sleep(30)
  del links [12]
  del links[10]
  #For each category, the items are parsed
  for link in links:
    link_url = (link['href'])
    full_link = "https://www.halted.com"+link_url
    category_name = link.font.text
    print(full_link)
    go_down_subcategories_HSC(full_link,category_name)

def go_down_subcategories_HSC(url, category_name):
  sleep_counter(SLEEP_TIME)
  soup = selenium_and_soup(url)

  table = soup.find("td", {"class" : "content"})
  table_body = table.table.tbody
  show_pictures_link = table_body.find("span", {"class" : "content"})
  if show_pictures_link != None:
    get_item_categories_with_pictures_HSC(url, category_name)
  else:
    table = soup.find("td", {"class" : "content"})
    all_tables = table.findAll("table", recursive=False)
    table_container = all_tables[1]
    rows = table_container.tbody.findAll("tr", recursive=False)
    row = rows[2].table.tbody
    items = row.findAll("tr")
    for item in items:
      link = "https://www.halted.com" + item.a['href']
      print(link)
      get_item_categories_with_pictures_HSC(link,category_name)
      # time.sleep(60)

def get_item_categories_with_pictures_HSC(url,category_name):
  print("Going to page with pictures")
  sleep_counter(SLEEP_TIME)
  soup = selenium_and_soup(url)

  table = soup.find("td", {"class" : "content"})
  table_body = table.table.tbody
  show_pictures_link = table_body.find("span", {"class" : "content"})
  picture_link_href = "https://www.halted.com" + show_pictures_link.a['href']
  recursive_page_turner_HSC(picture_link_href,category_name)
  # print(picture_link_href)


def recursive_page_turner_HSC(url,category_name):
  print("Images are displaying...")
  print("Using recursive page turner...")
  sleep_counter(SLEEP_TIME)
  soup = selenium_and_soup(url)

  get_HSC_rows(soup,category_name)

  form = soup.find("form", {"name" : "ProductForm"})
  print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nProduct Form Recursive Page Turner...")
  table_body = form.table.tbody.tr
  right_column = table_body.findAll("td")[2]
  link_container = right_column.span.findAll("a")
  print(link_container)
  time.sleep(10)
  if link_container != []:
    link_container_index = len(link_container) - 1
    last_link = link_container[link_container_index]
    last_link_text = last_link.text

    if "prev" not in last_link_text:
      print("There's a link on this page")
      next_page = "https://www.halted.com" +last_link['href']
      print(next_page)
      recursive_page_turner_HSC(next_page,category_name)

def get_HSC_rows(soup,category_name):
  table = soup.find("td", {"class" : "content"})
  table_body = table.form.table.tbody
  if table_body !=None:
    print("There's a table here")
    # print(table_body)
    rows = table_body.findAll('tr', recursive=False)
    del rows[0]
    del rows[0]
    list_index = len(rows)-1
    del rows[list_index]
    print(len(rows))

    for row in rows:
      row_container = row.td.table.tbody.tr.td.table.tbody
      print("\n\nNew Row")
      print(row_container)
      get_HSC_detail_info(row_container, category_name)

def get_HSC_detail_info(soup, category):
  rows = soup.findAll("tr", recursive=False)
  price_link_row = rows[1].td.table.tbody

  print("\n\nDESCRIPTION")
  uncut_desc = soup.find("span", {"class" : "title"}).text
  lowercase_desc = uncut_desc.lower()
  description_partition = lowercase_desc.partition('- was')
  desc = description_partition[0]
  print(desc)

  print("\n\nLINK")
  containers_list = price_link_row.findAll("tr", recursive=False)
  link_container = containers_list[1].find("a")['href']
  # print(link_container)
  link = "https://www.halted.com"+link_container
  # print(link)

  print("\n\nIMAGE")
  img = "https://www.halted.com"+soup.tr.td.img['src']
  print(img)
  # time.sleep(1)
  print("\n\nPRICE")
  price_container = price_link_row.tr.findAll("td", recursive=False)
  price = price_container[2].font.text.strip()
  print(price)

  print("\n\nSITENAME")
  sitename = "HSC Electronic Supply"
  print(sitename)

  print("\n\nCATEGORY")
  print(category)



def get_air_gas_items(url):

  soup = None
  sleep_counter(SLEEP_TIME)

  # browser = get_headless_selenium_browser()

  # browser = get_selenium_browser()
  # browser.get(url)
  # soup = BeautifulSoup(browser.page_source, "html.parser")

  soup = headless_selenium_and_soup(url)

  # page = Client(url)
  # soup = BeautifulSoup(page.html, "html.parser")

  if(soup == None):
    print("WHHHHHHYYYYYYY!!!")
    return None
  print(url)
  if(soup.find("li", {"class" : "sub-category-view2"}) == None):
    while(soup != None):
      for item in soup.findAll("div", {"class" : "search-result-row"}):
        try:
          # get desc
          desc = str(item.find("h3").string)
          print(desc)
          # get link
          link = "http://www.airgas.com" + str(item.find("a")['href'])
          print(link)
          # get img
          img = "http://www.airgas.com" + str(item.find("img")['src'])
          # get price
          price_cont = item.find("div", {"class" : "price-container"})
          price = str(price_cont.find("span", {"class" : "value"}).string).translate(str.maketrans('','','\n\t'))
          # get price unit
          price_unit = str(price_cont.find("span", {"class" : "unit"}).string).translate(str.maketrans('','','\n\t'))
          print(price_unit)
          # get category
          category = str(soup.find("h2", {"class" : "product-row-header"}).string)

          put_into_database(desc, link, img, price, "Airgas", category)
        except:
          print("Missing Some Stuff")
      soup = has_next(soup)

  else:
    for category in soup.findAll("li", {"class" : ["sub-category-view2", "sub-category-view3"]}):
      cat_url = category.a['href']
      get_air_gas_items("http://www.airgas.com" + cat_url)


def has_next(soup):

  next_container = soup.find("ul", {"class" : "results"})
  if(next_container != None):
    next = next_container.find("a", text=re.compile("NEXT"))
    if(next != None):
      url = str(next['href'])
      # page = Client("http://www.airgas.com" + url)
      # soup = BeautifulSoup(page.html, "html.parser")
      # browser = get_headless_selenium_browser()

      # browser = get_selenium_browser()
      # browser.get("http://www.airgas.com" + url)
      # soup = BeautifulSoup(browser.page_source, "html.parser")
      sleep_counter(4)
      soup = headless_selenium_and_soup("http://www.airgas.com" + url)

      return soup

  return None


def get_automation_direct_items(url, cat_name=""):
  soup = None
  sleep_counter(SLEEP_TIME)


  # soup = headless_selenium_and_soup(url)

  code = get_secure_connection(url)
  soup = BeautifulSoup(code.text, "html.parser")

  if(soup == None):
    print("WHHHHHHYYYYYYY!!!")
    return None

  elif(soup.find("a", {"class" : "itemLink gridLink selectedItemLink"}) != None):



    browser = get_selenium_browser()

    browser.get(url)
    page = browser.find_element_by_tag_name('html')
    page.send_keys(Keys.END)
    sleep_counter(2)
    page.send_keys(Keys.END)
    sleep_counter(2)
    page.send_keys(Keys.END)
    sleep_counter(2)
    page.send_keys(Keys.END)
    sleep_counter(2)


    code_text = get_scrapable_text(browser.page_source)
    soup = BeautifulSoup(code.text, "html.parser")

    soup_with_js = BeautifulSoup(code_text, "html.parser")
    print("ENDING STUFF")

    delimiter = ">"
    category_tree_container = soup.find("div", {"class" : "adcBreadCrumb"}).span
    category_tree = get_category_tree(category_tree_container,delimiter)
    print(category_tree)
    cat = category_tree
    # time.sleep(10000)

    try:


      sshtunnel.SSH_TIMEOUT = 550.0
      sshtunnel.TUNNEL_TIMEOUT = 550.0

      with sshtunnel.SSHTunnelForwarder('ssh.pythonanywhere.com',
                        ssh_username='iclam19',
                        ssh_password='@astest@1234',
                        remote_bind_address=('iclam19.mysql.pythonanywhere-services.com'
                        , 3306)) as tunnel:
        connection = mysql.connector.connect(user='iclam19',
          password='astest1234', host='127.0.0.1',
          port=tunnel.local_bind_port,
          database='iclam19$AssembledSupply')

        mycursor = connection.cursor()


        for product in soup_with_js.findAll("tr", {"class" : "dataRow"}):
          try:
            # get link
            link = product.find("a", {"class" : "listingLink"})
            link = str(link['href'])
            # get description
            desc = product.find("a", {"class" : "listingLink"}).string
            # get img
            img = product.find("img")['src']
            # get price
            price = product.find("span", {"id" : re.compile(r"price.*")}).string
            # get category
            cat_container = soup.find("a", {"class" : "itemLink gridLink selectedItemLink"})
            category = cat_container.find("span").string
            sitename = "Automation Direct"
            put_into_mysql_database(desc, link, img, price, sitename, cat, mycursor, connection)
            # time.sleep(1000)
          except:
            print("Database write didn't work")
        connection.close()

            # put_into_database(desc, link, img, price, "Automation Direct", category)

        return None
    except:
      write("Failed to initiate db write")

  elif(soup.find("td", {"class" : "notecomp_text"}) != None):
    print("Found the nocomp text class and returning none")
    time.sleep(10)
    return None

  else:
    for cat in soup.findAll("a", {"class" : ["cat-link", "itemLink"]}):
      print("DOIN STUFF DOWN HERE")
      cat_name = cat.img['alt']
      if(cat_name.find("Thumbnail") != None):
        cat_name = cat_name[:cat_name.find("Thumbnail")]
      get_automation_direct_items("https://www.automationdirect.com" + str(cat['href']), cat_name)


def get_scrapable_text(code_text):

  code = ""
  start = code_text.find("<tr style=\"background-color")
  end = code_text[start:].find("</tr>") + start + 5

  while(code_text[end:].find("class=\"dataRow\"") != -1):
    code += code_text[start:end] + "\n\n\n"
    start = code_text[end:].find("<tr style=\"background-color") + end
    end = code_text[start:].find("</tr>") + start + 5

  return code


#The Blackhawk Industrial crawler uses a recursive url based crawler
#to go deeper into each category. Once the crawler has reached a level with
#price information available, it searches that information and writes to the database.
#This code should probably be split into a couple different functions.
#At least, it would be clearer if the functionality dedicated to gathering
#item information once the crawler has reached the bottom page was split into
#its own function.


def get_blackhawk_industrial_items(url, cat_name=""):
  sleep_counter(SLEEP_TIME)
  soup = None
  soup = selenium_and_soup(url)

  print("Crawling using the Blackhawk Industrial crawler")
  if(soup == None):
    print("WHHHHHHYYYYYYY!!!")
    return None

  nav = soup.find("ul", {"class" : "sitemap collapse navbar-collapse navbar-wp mega-menu right"})

  if(nav != None):
    print("I found a navigator heading")
    category_list = nav.findAll("li", recursive=False)
    # print(category_list)
    # time.sleep(100)

    for category in category_list:
    # for category in nav.findAll("li"):
      # print("I wanna rock")
      # print(category)
      category_link = category.a['href']
      print("https://www.bhid.com/"+category_link)
      get_subcategories_recursive_blackhawk_industrial("https://www.bhid.com/"+category_link)

  else:
    print("I'm not sure what's happened here but it crashed on the homepage")


def get_subcategories_recursive_blackhawk_industrial(url):
  sleep_counter(4)

  browser = get_selenium_browser()
  browser.get(url)

  # time.sleep(50)


  code = browser.page_source
  soup = BeautifulSoup(code, "html.parser")


  cat_nav = soup.find("div", {"class" : "col-sm-9 col-xs-12 no-padding-right content-builder-overlay"})

  if(cat_nav != None):
    print("Found subcategories")
    subcategory_list = cat_nav.find("ul", {"class" : "categorycontent-container list-unstyled"})
    if(subcategory_list != None):
      for subcategory in subcategory_list.findAll("li"):
        subcategory_link = subcategory.a['href']
        if subcategory_link != "/CatSearch/4724/jobber-drills" and subcategory_link != "/CatSearch/4718/high-performance-drills":
          print(subcategory_link)
          get_subcategories_recursive_blackhawk_industrial("https://www.bhid.com/"+subcategory_link)
    else:

      print("I'm on a page with a bunch of products...")

      items_per_page_selector = soup.find("button", {"id" : "selItemsPerPage"}).text.strip()
      print(items_per_page_selector)
      print("\n\n")
      # time.sleep(10)

      if items_per_page_selector != "42":
        print("It's not 42 so it needs to be changed")
        results_per_page_dropdown = browser.find_element_by_id("selItemsPerPage")
        results_per_page_dropdown.click()
        results_per_page_list = browser.find_elements_by_class_name("search-results-per-page")
        forty_two_per_page = results_per_page_list[-1]
        time.sleep(1)
        forty_two_per_page.click()

        code = browser.page_source
        soup = BeautifulSoup(code, "html.parser")
        cat_nav = soup.find("div", {"class" : "col-sm-9 col-xs-12 no-padding-right content-builder-overlay"})

      else:
        print("it's 42 we're good to go man")

      page_advance_links = cat_nav.find("div", {"class" : "SearchResultPaging"})
      if page_advance_links != None:
        page_advance_link_list = page_advance_links.findAll("a")

        del page_advance_link_list[0]
        #From here there are a couple ways to go forward. I shouldn't make the next part recursive
        #or it will call itself infinitely. But I could make it break whenever I'm on the last page
        #However I have a better idea. I should just do it normally. Time for Dummy code:
        last_page_boolean = False

        while last_page_boolean == False:
          #Scroll to bottom of page
          total_pages_results = None
          while total_pages_results == None:
            #Resets soup so that
            code = browser.page_source
            soup = BeautifulSoup(code, "html.parser")
            cat_nav = soup.find("div", {"class" : "col-sm-9 col-xs-12 no-padding-right content-builder-overlay"})

            total_pages_results = soup.find("span", {"class" : "total-pages-results"})
          number_of_results = total_pages_results['data-count']
          # number_of_results = total_pages_results.data-count
          print(number_of_results)
          # time.sleep(10)

          if number_of_results != "0":
            # browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            #Get item info for whatever page we're on
            try:
              get_item_info_blackhawk_industrial(soup)
            except:
              print("Failed to get item info")



            page_advance_links = cat_nav.find("div", {"class" : "SearchResultPaging"})
            if page_advance_links != None:
              page_advance_link_list = page_advance_links.findAll("a")
              last_page_text = page_advance_link_list[-1].text.strip()
              print(last_page_text)
              # time.sleep(10)
              if last_page_text != "NEXT »":
                last_page_boolean = True
                # print("Caught the next page link")
                # time.sleep(100)

            if last_page_boolean != True:
              search_paging_container = browser.find_element_by_class_name("SearchResultPaging")
              pages_list = search_paging_container.find_elements_by_tag_name("a")
              last_page = pages_list[-1]
              print(last_page)
              # browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
              # browser.execute_script("window.scrollTo(0, window.scrollY + 200)")
              try:
                last_page.click()
              except:
                print("Handling exception. Scrolling down now")
                # time.sleep(10)
                browser.execute_script("window.scrollTo(0, window.scrollY + 200)")
                time.sleep(1)
                last_page.click()
          else:
            print("The page is empty yo")
            return
            last_page_boolean = True
            # time.sleep(1000)



            # time.sleep(1000)


        # number_of_pages = len(page_advance_link_list) -1
        # for i in range(number_of_pages):
        #   item_page = page_advance_link_list[i]
        #   item_page_link = item_page["href"]
        #   print(item_page_link)
        #   time.sleep(5)
        #   if item_page_link == "#":
        #     # soup = selenium_and_soup(url+item_page_link)
        #     open_pages_blackhawk_industrial(url+item_page_link)

        #     # browser.get(url+item_page_link)
        #   else:
        #     # soup = selenium_and_soup("https://www.bhid.com/"+item_page_link)
        #     open_pages_blackhawk_industrial("https://www.bhid.com/"+item_page_link)


      else:
        print("There's just one page")
        # return
        # try:
        get_item_info_blackhawk_industrial(soup)
        # except:
          # print("Used an exception")


def open_pages_blackhawk_industrial(url):
  sleep_counter(4)
  soup = selenium_and_soup(url)
  try:
    get_item_info_blackhawk_industrial(soup)
  except:
    print("Failed to get item info")


def get_item_info_blackhawk_industrial(soup):
  print("On a page with a bunch of items and I'm ready to drink their soup and get their item information sir")
  sitename = "Blackhawk Industrial"
  # time.sleep(100000)

  category_tree_container = soup.find("div", {"class" : "SearchResultsLblInfo"}).span
  delimiter = "»"
  category_tree = get_category_tree(category_tree_container,delimiter)
  print(category_tree)
  # time.sleep(1000)


  category = category_tree
  # category_container = soup.find("div", {"class" : "col-sm-9 col-xs-12 no-padding-right content-builder-overlay"})
  # category = category_container.h1.text

  # print(category)

  # connection = connect_to_tunnel()

  #It would be excellent to put this code in its own function, but I'm not sure how
  #The connection automatically closes when the function that it's inside finishes.

  sshtunnel.SSH_TIMEOUT = 550.0
  sshtunnel.TUNNEL_TIMEOUT = 550.0

  with sshtunnel.SSHTunnelForwarder('ssh.pythonanywhere.com',
                    ssh_username='iclam19',
                    ssh_password='@astest@1234',
                    remote_bind_address=('iclam19.mysql.pythonanywhere-services.com'
                    , 3306)) as tunnel:
    connection = mysql.connector.connect(user='iclam19',
      password='astest1234', host='127.0.0.1',
      port=tunnel.local_bind_port,
      database='iclam19$AssembledSupply')

    mycursor = connection.cursor()


    item_list_container = soup.find("div", {"class" : "SKULineOuterWrapper"})
    item_list = item_list_container.findAll("div", {"class" : "SKULineWrapper"})
    for item in item_list:
    # print(item)
      sku_description = item.find("div", {"class" : "SKULineDescInfo"})
      description = sku_description.h2.a.text
      link = "https://www.bhid.com" + sku_description.h2.a['href']
    # print(description)
    # print(link)
    # time.sleep(1000)
      image_container = item.find("div", {"class" : "ProductImagesContainerInner"})
      image_source_a = image_container.a
      if image_source_a == None:
        image_source = "https://www.bhid.com" + image_container.div.a['href']
      else:
        image_source = "https://www.bhid.com" + image_source_a['href']

      # print(image_source)
      price_container = item.find("span", {"class" : "PriceBreaks"})
      if price_container != None:
        price = price_container.text
        # print(price)
        # time.sleep(1000)
        # put_into_database(description, link, image_source, price, sitename, category)
      # try:
        put_into_mysql_database(description, link, image_source, price, sitename, category, mycursor, connection)
      # except:
        # print("Db write failed")
    connection.close()







# def get_blackhawk_industrial_items(url, cat_name=""):
#   sleep_counter(SLEEP_TIME)
#   soup = None
#   soup = selenium_and_soup(url)

#   # browser = get_selenium_browser()
#   # browser.get(url)
#   # code = browser.page_source
#   # soup = BeautifulSoup(code, "html.parser")


#   print("Crawling using the Blackhawk Industrial crawler")
#   if(soup == None):
#     print("WHHHHHHYYYYYYY!!!")
#     return None
#   cat_nav = soup.find("div", {"class" : "col-sm-9 col-xs-12 no-padding-right content-builder-overlay"})
#   nav = soup.find("ul", {"class" : "sitemap collapse navbar-collapse navbar-wp mega-menu right"})
#   if(cat_nav != None):
#     print("Found subcategories")
#     subcategory_list = cat_nav.find("ul", {"class" : "categorycontent-container list-unstyled"})
#     if(subcategory_list != None):
#       for subcategory in subcategory_list.findAll("li"):
#         subcategory_link = subcategory.a['href']
#         print(subcategory_link)
#         get_blackhawk_industrial_items("https://www.bhid.com/"+subcategory_link)
#     else:
#       print("I'm on a page with a bunch of products...")

#       page_advance_links = cat_nav.find("div", {"class" : "SearchResultPaging"})
#       if page_advance_links != None:
#         page_advance_link_list = page_advance_links.findAll("a")

#         #From here there are a couple ways to go forward. I shouldn't make the next part recursive
#         #or it will call itself infinitely. But I could make it break whenever I'm on the last page
#         #However I have a better idea. I should just do it normally. Time for Dummy code:
#         number_of_pages = len(page_advance_link_list) -1
#         for i in range(number_of_pages):
#           item_page = page_advance_link_list[i]
#           item_page_link = item_page["href"]
#           print(item_page_link)
#           time.sleep(5)
#           soup = None
#           # browser = get_selenium_browser()
#           if item_page_link == "#":
#             soup = selenium_and_soup(url+item_page_link)
#             print(soup)
#             # time.sleep(1000)
#             # browser.get(url+item_page_link)
#           else:
#             # browser.get("https://www.bhid.com/"+item_page_link)
#             soup = selenium_and_soup("https://www.bhid.com/"+item_page_link)
#           # code = browser.page_source
#           # soup = BeautifulSoup(code, "html.parser")

#           category_container = soup.find("div", {"class" : "col-sm-9 col-xs-12 no-padding-right content-builder-overlay"})
#           category = category_container.h1.text
#           print(category)


#         item_list_container = soup.find("div", {"class" : "SKULineOuterWrapper"})
#         item_list = item_list_container.findAll("div", {"class" : "SKULineWrapper"})
#         for item in item_list:
#           item_info = item.find("div", {"class" : "SKULineDescInfo"})
#           item_info_link = item_info.h2.a['href']
#           time.sleep(5)
#           soup = None
#           item_page_soup = selenium_and_soup("https://www.bhid.com/"+item_info_link)
#           # browser = get_selenium_browser()
#           # browser.get("https://www.bhid.com/"+item_info_link)
#           # code = browser.page_source
#           # item_page_soup = BeautifulSoup(code, "html.parser")
#           print("I'm on an item page now!")
#           sku_container = item_page_soup.find("div", {"class" : "SKUDetailRight"})
#           sku_price = sku_container.find("div", {"class" : "SKUProductInfo"})
#           if sku_price.div.a == None:
#             print("There should be a price here")
#             price = sku_price.div.span.string
#             print("I GOTTA THE PRICE MARIO")
#             print(price)
#             print("I GOTTA THE PRICE MARIO")
#             sku_description = sku_container.find("div", {"id" : "detail-header"})
#             description = sku_description.h1.string
#             print(description)
#             link = "https://www.bhid.com/"+item_info_link
#             sitename = "Blackhawk Industrial"
#             picture_container = item_page_soup.find("div", {"class" : "SKUDetailLeft"})
#             picture_relative_link = picture_container.div.a.img['src']
#             if picture_relative_link == None:
#               image_source = ""
#             else:
#               image_source = "https://www.bhid.com/"+picture_relative_link
#             put_into_database(description, link, image_source, price, sitename, category)

#             # print("\n\nCATEGORY")




#           else:
#             print("Price requests must be made specially for this item")


#   elif(nav != None):
#     print("I found a navigator heading")
#     for category in nav.findAll("li"):
#       print("I wanna rock")
#       # print(category)
#       category_link = category.a['href']
#       print("https://www.bhid.com/"+category_link)
#       get_blackhawk_industrial_items("https://www.bhid.com/"+category_link)


#Directools Crawler Notes:
#The directools parser uses a recursive page turner to
#browse through all the pages of each category. Because the
#number of items displayed per page can be controlled through
#a url entry, and because each page within a category has a distict
#url, and not simply an ajax call to change pages, there is no
#selenium "click" functionality required for this browser.
#The information parsing is built into the same function as the
#recursive page turner.

def get_directools_items(url, name=""):
  soup = None
  sleep_counter(7)
  sitename = "Directools"
  # page = Client(url)
  browser = get_selenium_browser()
  browser.get(url)
  code = browser.page_source
  # print(code)
  soup = BeautifulSoup(code, "html.parser")



  if(soup == None):
    print("WHHHHHHYYYYYYY!!!")
    return None

  nav_list = soup.find("ul", {"id" : "category_nav_ad"})
  if nav_list != None:
    print("Homepage")
    categories = nav_list.findAll("li", {"class" : ["category first sub-cat-nav li l0","category sub-cat-nav li l0"]})
    print(categories)
    for category in categories :
      category_link = "https://www.directools.com/"+category.a['href']+"&pg=1&items_per_page=200"
      directools_recursive_page_turner(category_link)


def directools_recursive_page_turner(url, name=""):
  print("I'm using the recursive page turner")
  sitename = "Directools"
  sleep_counter(8)
  # page = Client(url)
  browser = get_selenium_browser()
  browser.get(url)
  code = browser.page_source
  # print(code)
  soup = BeautifulSoup(code, "html.parser")

  table = soup.find("table", {"id" : "search_list"})
  try:

    table_body = table.tbody
    items = table_body.findAll("tr")
    for item in items:
      print("DESCRIPTION")
      description = item.find("td", {"class" : "description"})
      desc = description.text.strip()
      print(desc)
      print("\n\nLINK")
      link_container = item.find("td", {"class" : "item_code"})
      link = "https://www.directools.com/" + link_container.a['href']
      print(link)
      print("\n\nIMAGE")
      image_container = item.find("td", {"class" : "image"})
      img_box = image_container.div.div


      print("img")
      if img_box == None:
        source_box = image_container.div.a
        image = source_box.find("img")
        img = "https://www.directools.com/" + image['src']
      else:
        print(img_box)
        img_tag = img_box.find("img")
        img = "https://www.directools.com/" + img_tag['src']

      print("\n\nPRICE")
      price_container = item.find("td", {"class" : "price"})
      price = price_container.text
      print(price)
      print("\n\nSITENAME")
      print(sitename)
      print("\n\nCATEGORY")
      category_container = soup.find("span", {"class" : "header-text"})
      category = category_container.text
      print(category)

      put_into_database(desc, link, img, price, sitename, category)


    #Find the navigator
    navigator = soup.find("ul", {"class" : "pagination pull-right no_top_margin"})
    #Go to the next page
    Next_page = navigator.find("li", {"class" : "pagination_next "})
    if Next_page !=None:
      Next_page_link ="https://www.directools.com/search/" + Next_page.a['href']
      print("Link to next page")
      print(Next_page_link)
      print("Link to next page")
      browser.quit()
      directools_recursive_page_turner(Next_page_link)
    else:
      print("It's empty")
  except:
    print("Nothing on this page")


#The baileigh industrial crawler uses standard url crawling
#without additional selenium functionality. Item information is
#available from the list pages (visiting the individual item pages
#is not required to gather info), so the parsing time is very short.

def get_baleigh_industrial_items(url, name=""):
  soup = None
  sleep_counter(SLEEP_TIME)
  print("Baleigh Industrial")
  sitename = "Bailiegh Industrial"
  # page = Client(url)
  browser = get_selenium_browser()
  browser.get(url)
  code = browser.page_source
  # print(code)
  soup = BeautifulSoup(code, "html.parser")



  if(soup == None):
    print("WHHHHHHYYYYYYY!!!")
    return None

  nav_list = soup.find("div", {"class" : "col-main"})
  if nav_list != None:
    print("Category Page")
    categories = nav_list.findAll("div", {"class" : "category-listing"})
    print("Categories")
    print(categories)
    print("Categories")
    if categories == []:
      category_container = soup.find("div", {"class" : ["page-title category-title background","page-title category-title"]})
      category = category_container.h1.text
      print("We're on a page that has items")

      category_tree_container = soup.find("div", {"class" : "breadcrumbs"})
      delimiter = "/"
      category_tree = get_category_tree(category_tree_container, delimiter)
      print(category_tree)
      # time.sleep(1000)
      cat = category_tree

      product_list = nav_list.find("ol", {"class" : "products-list"})
      try:
        items = product_list.findAll("li", {"class" : ["item","item last"]})


        sshtunnel.SSH_TIMEOUT = 550.0
        sshtunnel.TUNNEL_TIMEOUT = 550.0

        with sshtunnel.SSHTunnelForwarder('ssh.pythonanywhere.com',
                          ssh_username='iclam19',
                          ssh_password='@astest@1234',
                          remote_bind_address=('iclam19.mysql.pythonanywhere-services.com'
                          , 3306)) as tunnel:
          connection = mysql.connector.connect(user='iclam19',
            password='astest1234', host='127.0.0.1',
            port=tunnel.local_bind_port,
            database='iclam19$AssembledSupply')

          mycursor = connection.cursor()



          for item in items:
            # print("\n\nITEM")
            # print(item)
            # print("DESCRIPTION")
            description_header = item.find("h2", {"class" : "product-name"})
            desc = description_header.a['title']
            # print(desc)
            # print("\n\nLINK")
            link = description_header.a['href']
            # print(link)
            # print("\n\nIMAGE")
            img = item.find("img", {"class" : "lazy-load"})['data-src']
            # print(img)
            # print("\n\nPRICE")
            price_box = item.find("div", {"class" : "price-box"})
            if price_box is not None:
              price_span = price_box.span
              if price_span is not None:
                try:
                  price = price_box.span['content']
                  # print(price)
                  # print("\n\nSITENAME")
                  # print(sitename)
                  # print("\n\nCATEGORY")
                  # print(category)

                  put_into_mysql_database(desc, link, img, price, sitename, cat, mycursor, connection)
                  # time.sleep(1000)

                  # put_into_database(desc, link, img, price, sitename, cat)

                except KeyError:
                  print("No Price Available")
          connection.close()
      except:
        print("Empty page. useless")

    for category in categories :
      category_link = category.h2.a['href']
      print(category_link)
      get_baleigh_industrial_items(category_link)

#The QC Industrial crawler works on one category of QC supply.
#QC supply has several fields they supply for, and most of them are
#irrelevant to AssembledSupply's current market, and are therefore not
#parsed. The QC crawler operates by repeatedly moving to the next page
#using a recursive page turner which operates using urls (not selenium clicking).
def get_qc_industrial_items(url, name=""):
  print("THIS IS THE URL")
  print(url)

  soup = None
  sleep_counter(SLEEP_TIME)
  print("QC Supply")
  sitename = "QC Supply"
  # page = Client(url)
  browser = get_selenium_browser()
  browser.get(url)
  code = browser.page_source
  # print(code)
  soup = BeautifulSoup(code, "html.parser")

  browser.quit()

  if(soup == None):
    print("WHHHHHHYYYYYYY!!!")
    return None


  print("Open item pages")
  product_list = soup.find("ol", {"class" : "products list items product-items clearer"})
  items = product_list.findAll("li", {"class" : "item product product-item"})

  for item in items:
    print("Item HTML")
    # print(item)
    link = item.find("a", {"class" : "product-item-link"})
    link_page = link['href']
    print("<--------- Link to Page -------->")
    print(link_page)
    try:
      get_QC_Supply_info(link_page)
    except:
      print("123456789")
      print(link_page)
      print("123456789")


  nav_list_container = soup.find("div", {"class" : "toolbar-top"})
  if nav_list_container != None:
    print("Category Page")
    categories = nav_list_container.find("ul", {"class" : "items pages-items"})
    next_category = categories.find("li", {"class" : "item pages-item-next"})
    if next_category != None:
      next_category_link = next_category.a['href']
      print(next_category_link)
      get_qc_industrial_items(next_category_link)
    else:
      print("No more pages after this one")


def get_QC_Supply_info(url):
  soup = None
  sleep_counter(SLEEP_TIME)
  print("QC Supply")
  sitename = "QC Supply"
  # page = Client(url)
  browser = get_selenium_browser()
  browser.get(url)
  code = browser.page_source
  # print(code)
  soup = BeautifulSoup(code, "html.parser")
  browser.quit()

  # print("THANOS DID NOTHING WRONG")
  # time.sleep(10)
  category_tree_container = soup.find("div", {"class" : "breadcrumbs"}).ul
  category_tree = get_category_tree(category_tree_container)
  print(category_tree)
  # time.sleep(1000)
  cat = category_tree



  sshtunnel.SSH_TIMEOUT = 550.0
  sshtunnel.TUNNEL_TIMEOUT = 550.0

  with sshtunnel.SSHTunnelForwarder('ssh.pythonanywhere.com',
                    ssh_username='iclam19',
                    ssh_password='@astest@1234',
                    remote_bind_address=('iclam19.mysql.pythonanywhere-services.com'
                    , 3306)) as tunnel:
    connection = mysql.connector.connect(user='iclam19',
      password='astest1234', host='127.0.0.1',
      port=tunnel.local_bind_port,
      database='iclam19$AssembledSupply')

    mycursor = connection.cursor()

    try:
      print("DESCRIPTION")
      description = soup.find("div", {"class" : "page-title-wrapper product"})
      desc = description.h1.text.strip()
      print(desc)
      print("\n\nLINK")
      link = url
      print(link)
      print("\n\nIMAGE")
      image_container = soup.find("div", {"class" : "fotorama__stage__shaft"})
      img = image_container.div.img['src']
      print(img)
      print("\n\nPRICE")


      price_container = soup.find("span", {"class" : "price-container price-final_price tax weee"})
      price = "$" + price_container.span['data-price-amount']
      decimal_index = price.find(".")
      length_of_price_string = len(price)
      decimal_location_correct = length_of_price_string -3
      print(price)
      print("Decimal Index")
      print(decimal_index)
      print("Decimal locationcorrect")
      print(decimal_location_correct)
      if decimal_index == -1:
        price = price + ".00"
      elif decimal_index != decimal_location_correct:
        print("yo")
        price = price + "0"
      print(price)
      # browser.quit()
      # time.sleep(10)
    except:
      print("Missing some stuff")
      connection.close()
      # browser.quit()
      return

    print("\n\nSITENAME")
    print(sitename)
    print("\n\nCATEGORY")
    # heading_categories = soup.find("ul", {"class" : "items"})
    # categories = heading_categories.findAll("li")
    # number_of_categories = len(categories)
    # print(number_of_categories)
    # sub_category = categories[number_of_categories - 1]
    # category = sub_category.a.text
    # print(category)

    # put_into_database(desc, link, img, price, sitename, category)
    put_into_mysql_database(desc, link, img, price, sitename, cat, mycursor, connection)
    connection.close()
    # time.sleep(1000)
    # browser.quit()

#The online metals browser uses a standard url web crawler
#with some selenium functionality. Selenium is used to click different
#size options and "add to cart" in order to retrieve price information.
#Recursion is used to crawl deeper into each category, but a page turner
#is not used (item categories are small enough to display all items on
#a single page).
def get_online_metals_items(url, name=""):
  soup = None
  sleep_counter(SLEEP_TIME)
  print("Online Metals")
  sitename = "Online Metals"
  # page = Client(url)
  browser = get_selenium_browser_random_proxy()
  browser.get(url)
  code = browser.page_source
  # print(code)
  soup = BeautifulSoup(code, "html.parser")


  if(soup == None):
    print("WHHHHHHYYYYYYY!!!")
    return None

  print("Open item pages")
  product_table = soup.find("table", {"id" : "cattable"})
  table_rows = product_table.findAll("tr")
  for row in table_rows:
    items = row.findAll("ul", {"id" : "catbutton"})
    for item in items:
      link = item.a['href']
      print(link)
      product_page_browsing_online_metals(link)

def product_page_browsing_online_metals(url):
  soup = None
  sleep_counter(4)
  print("Online Metals")
  sitename = "Online Metals"
  # page = Client(url)
  browser = get_selenium_browser_random_proxy()
  browser.get(url)
  code = browser.page_source
  # print(code)
  soup = BeautifulSoup(code, "html.parser")

  category_table = soup.find("div", {"class" : "product-subcats clearfix"})
  if category_table != None:
    category_columns = category_table.findAll("div", {"class" : "cat-col"})
    for column in category_columns:
      link_list = column.findAll("a")
      for link in link_list:
        link_source = link['href']
        print(link_source)
        product_page_browsing_online_metals(link_source)
  else:
    print("We're on a page with individual items")
    print("Getting information for individual items")
    category_container = soup.find("div", {"id" : "product-intro"})
    category = category_container.h1.text
    print(category)
    items_table = soup.find("ul", {"id" : "inches"})
    item_columns = items_table.findAll("div", {"id" : "half-col"})
    for column in item_columns:
      items_list = column.findAll("p")
      for item in items_list:
        item_link = item.b.a['href']
        print(item_link)
        get_product_info_online_metals(item_link, category)


    # get_product_info_online_metals(url)

def get_product_info_online_metals(url,category):
  soup = None
  sleep_counter(4)
  print("Online Metals")
  sitename = "Online Metals"
  # link = url
  link = "https://www.onlinemetals.com/"+url
  print(link)
  # page = Client(url)
  browser = get_selenium_browser_random_proxy()
  browser.get(link)
  time.sleep(3)
  code = browser.page_source
  # print(code)
  soup = BeautifulSoup(code, "html.parser")
  if soup == None:
    print("WHYYYY")

  print("\n\nLINK")
  print(link)
  print("\n\nIMAGE")
  picture = soup.find("div", {"id" : "feature"})
  try:

    img = picture.img['src']
    print(img)

    print("\n\nSITENAME")
    print(sitename)
    print("\n\nCATEGORY")
    print(category)


    add_to_cart = browser.find_element_by_id("add-to-cart")
    print(add_to_cart)


    size_selection_boxes = browser.find_elements_by_class_name("available-size")
    print(len(size_selection_boxes))
    if size_selection_boxes == []:
      print("There's nothing here")
    time.sleep(3)

    for li in size_selection_boxes:
      time.sleep(1)
      window_before = browser.window_handles[0]
      li.click()
      time.sleep(5)
      print("should've clicked the link")
      ActionChains(browser) \
      .key_down(Keys.CONTROL) \
      .click(add_to_cart) \
      .key_up(Keys.CONTROL) \
      .perform()
      # newwin.keyDown(Keys.SHIFT).click(li).keyUp(Keys.SHIFT).build().perform();

      # li.click()
      print("There can only be one thing to click")
      time.sleep(3)
      window_after = browser.window_handles[1]
      browser.switch_to_window(window_after)
      # browser.get("Second URL");
      print("Im on the second browser")
      time.sleep(2)

      code = browser.page_source
      soup = BeautifulSoup(code, "html.parser")
      print("\n\nDESCRIPTION")
      table = soup.find("table", {"id" : "order-summary-table"})
      description_column = soup.find("td", {"class" : "nobottompadding"})
      desc = description_column.h5.strong.a.text
      print(desc)
      print("\n\nPRICE")
      row_container = soup.find("tr", {"class" : "nobottomborder"})
      columns = row_container.findAll("td")
      price_column_index = len(columns)-1
      price_column = columns[price_column_index]
      price = price_column.span.text.strip()
      print(price)

      delete_item_from_cart = browser.find_elements_by_class_name("hide-row")
      for item in delete_item_from_cart:
        item.click()

      browser.close()
      browser.switch_to_window(window_before)

      put_into_database(desc, link, img, price, sitename, category)
    browser.quit()
  except:
    browser.quit()


#The fastener superstore crawler uses a url based crawler with a
#selenium-driven recursive page-turner. The subcategories section of
#the crawler is recursive, as the subcategories are sometimes multiple
#levels deep. Finally, the recursive page turner uses a selenium "click"
#operation, as the url does not change when the "turn-page" option is
#used.
def get_fastener_superstore_items(url, name=""):
  print("Home Page")
  sleep_counter(SLEEP_TIME)
  supplier = "Fastener Superstore"
  # print(url)
  soup = headless_selenium_and_soup(url)
  print(soup)
  # time.sleep(1000)

  category_container = soup.find("section", {"class" : "category_list inner_col"})
  for category in category_container.findAll("li"):

    # print(category)
    print("DOIN STUFF DOWN HERE")
    cat_name = str(category.find("h2").string).translate(str.maketrans('','',' \n\t'))
    print(cat_name)
    get_fastener_superstore_subcategories("https://www.fastenersuperstore.com/" + str(category.find("a")['href']))
    # get_fastener_superstore_items("https://www.fastenersuperstore.com/" + str(category.find("a")['href']), cat_name)


def get_fastener_superstore_subcategories(url):
  print("Category Page")
  sleep_counter(SLEEP_TIME)
  soup = headless_selenium_and_soup(url)

  if(soup == None):
    print("WHHHHHHYYYYYYY!!!")
    return None

  category_container = soup.find("section", {"class" : "category_list"})
  if category_container != None:
    category_list = category_container.findAll("li")
    if len(category_list) > 6:
      print("it's less than 1000")
      # time.sleep(10000)
      for i in range(6):
        print(i)
        del category_list[0]
      # time.sleep(10)
    # print("Not at subcategories yet")
    # del category_container[0]
    for category in category_list:
      print("TIddleywodnks")
      print("DOIN STUFF DOWN HERE")
      cat_name = str(category.find("h2").string).translate(str.maketrans('','',' \n\t'))
      print(cat_name)
      # time.sleep(1000)
      get_fastener_superstore_subcategories("https://www.fastenersuperstore.com/" + str(category.find("a")['href']))
      # get_fastener_superstore_items("https://www.fastenersuperstore.com/" + str(category.find("a")['href']), cat_name)
  else:
    time.sleep(4)
    print("On a page with Subcategories")
    category = soup.find("div", {"class" : "col-sm-5"})
    filters = category.findAll("li")
    print(category)
    if len(filters) > 1:
      print(filters[0])
      # time.sleep(1000)
      del filters[0]
    for filter in filters:
      cat_name = filter.a['href']
      # cat_name = str(category.find("a").string).translate(str.maketrans('','',' \n\t'))
      print(cat_name)
      browser = get_selenium_browser()
      browser.get("https://www.fastenersuperstore.com/" + cat_name)

      fastener_superstore_page_turner("https://www.fastenersuperstore.com/" + cat_name, browser)

def fastener_superstore_page_turner(url, browser):
  print("I'm on a page with many items")
  print(url)
  sleep_counter(1)

  page = "NotLast"
  while page != "last":
    soup = None
    # browser = get_selenium_browser()
    # browser.get(url)
    code = browser.page_source
    soup = BeautifulSoup(code, "html.parser")
    # print(soup)
    if (soup == None):
      print("NO Dang Soup In the Whole Damn Town")


    rows = soup.findAll("div", {"class" : ["common_row","common_row odd"]})

    for row in rows:
      # print(row)
      # time.sleep(10)
      try:
        row_link = row.find("a")['href']
        link = "https://www.fastenersuperstore.com/" + row_link
        print(row_link)
        get_product_info_fastener_superstore(link)
      except:
        pass

        #Recursive Bit
    # print("This is where the recursive part needs to come in...")

    page_turning = soup.find("div", {"class" : "paging top"})
    if page_turning != None:
      print("Turning the page again")
      print(page_turning)
      page_list = [1]
      page_list = page_turning.findAll("li")
      i = 0
      active_list_index = 0
      for page in page_list:
        print(page)
        try:
          page_class = page['class']
          print("This is the page class")
          if page_class == ["active"]:
            print("We gotta one!")
            print(page_class)
            active_list_index = i

        except:
          print("No class associated to this link")
          time.sleep(1)
        i = i+1
        #If the active path index +1 is not equal to the length of the list
        #Then we aren't on the last page, and therefore we need to go again
      if (active_list_index+1) != len(page_list):
        print("There are more pages to turn")
        #GEt the element to click using the browser variable
        #Click it
        #Run yourself again!
        selenium_list_elements = browser.find_elements_by_class_name("pagination")
        element_to_click = selenium_list_elements[active_list_index+1]
        print(active_list_index)
        element_to_click.click()
        time.sleep(3)
      else:
        page = "last"
        print(page)
        time.sleep(3)
    else:
      page = "last"
      time.sleep(3)
        # fastener_superstore_recursive_page_turner(url, browser)
        # browser.page_source
        # next_page = driver.find_element_by_xpath("//p[@id='one']/following-sibling::li")


def get_product_info_fastener_superstore(url):
  time.sleep(3)
  print("Individual Item Page")
  print(url)
  soup = headless_selenium_and_soup(url)
  supplier = "Fastener Superstore"

  if(soup.find("div", {"class" : "pic_box"}) != None):
    product = soup.find("div", {"class" : "product_details"})
    link = url
    print(link)
    description = soup.find("section", {"class" : "product_page"})
    desc = description.h1.text

    # desc = product.find("a", {"class" : "listingLink"}).string

    # get img
    img = product.find("img")['src']
    print("THIS IS RIGHT BEFORE IMAGE TAG")
    # time.sleep(100000)
    print("Image TAG")
    print(img)
    print("Image TAG")
    tables = product.findAll("div", {"class" : "box_row"})

    price_table = (tables[1])

    column = price_table.find("span", {"class" : "col_box big"})
    print(column)
    print(column.strong.text)


    # THIS WHOLE SEGMENT OF CODE IS FUCKING OUT ON ME AND IM NOT SURE WHY. IT WONT RUN THIS PRINT STATEMENT

    price_str = column.strong.text
    print("ALRIGHTY THEN COWBOYS")
    # time.sleep(1000)

    unit = ""
    #Price Splitting
    try:
      partition = price_str.partition('/')
      price = partition[0]
      print(price)
      unit_with_spaces = partition[2].strip()
      unit = " ".join(unit_with_spaces.split())
      print(unit)
    except:
      price = price_str

    category_string = soup.find("ul", {"class" : "breadcrumb"})
    categories = category_string.findAll("li")
    a = len(categories) - 1
    print("Tiddlywinks")
    print(a)
    print("Tiddlywinks")
    category_link = categories[a]
    print(category_link)
    category_name = category_link.find("a").text
    print("Category")
    # category_link_html_complete = "https://www.fastenersuperstore.com/"+category_link_html
    print(category_name)
    print("Category Link")
    print("\n\n WHAT THE FUCK MAN \n\n")
    put_into_database(desc, link, img, price, supplier, category_name,unit)

  else:
    pass




#This Section For Generically Handling Scraping Operations

def get_category_tree(category_soup,delimiter="|"):

  #Splitting this process into generic steps:

  #1. Define all the text delimiters that you want to remove from your text
  text_delimiters = ["\n"," Now In: "]


  #1. Get all the text you need.
  tags = category_soup.findAll()
  category_name_bottom = ""
  text_list = []
  for tag in tags:
    if hasattr(tag, 'text'):
      text = tag.text.strip()
      #If there are multiple of the the delimeters in the first block of text,
      #then that first block contains all the info you need. So only run the for
      #loop if this is not the case
      counter = text.count(delimiter)
      if counter >1:
        for item in text_delimiters:
          text = text.replace(item,"")
        category_name_bottom = text
        text_list = [0]
      else:
      #Otherwise, start by splitting up the text by the delimiter specific to
      #each webiste
        for item in text_delimiters:
          text = text.replace(item,"")
          text_split_based_on_delimiter = text.split(delimiter)
          for text_replace in text_split_based_on_delimiter:
            #Add to new list, removing duplicates in process
            if text_replace.strip() not in text_list:
              text_list.append(text_replace.strip())

  print(text_list)
  # time.sleep(10000)
  # print("This is category name bottom")
  # print(category_name_bottom)
  # print("Taht was category name bottom")
  # time.sleep(100)
  if text_list[0] != 0:
    for text in text_list:
      if delimiter not in text:
        print("Delimiter not in text")
        print(text)
        if category_name_bottom != "":
          category_name_bottom = category_name_bottom + delimiter + text.strip()
        else:
          category_name_bottom = category_name_bottom + text.strip()
        print("THIS IS THE FULL CAT NAME THUS FAR")
        print(category_name_bottom)
      else:
        print("Delimiter in text")
        #If there is a delimiter in the text:
        print(text)
        #Get Rid of the Delimiter
        if text != delimiter:
          text = text.replace(delimiter, "")
          print(text)
          #Add text with a delimiter in it
          if category_name_bottom != "":
            category_name_bottom = category_name_bottom + delimiter + text.strip()
          else:
            category_name_bottom = category_name_bottom + text.strip()
          print("THIS IS THE FULL CAT NAME THUS FAR")
          print(category_name_bottom)

  print(category_name_bottom)
  # time.sleep(10000)
  # text = category_soup.findAll("text")



  # if hasattr(category_soup, 'text'):
  # # if category_soup.text:
  #   category_name_bottom = category_soup.text
  #   print(category_name_bottom)
  #   print("That was the bottom one")


  #2. Split the text by delimiters
  category_tree_list = category_name_bottom.split(delimiter)


  #3. Set delimiters so that extraneous items do not get added to the list
  delimiters = ["Home", "HOME", "home"]


  #4. Start the string concatenation by creating a blank entry
  category_tree = ""

  #5. Add the items if they do are not in the delimiters
  for category_level in category_tree_list:
    if(category_level.strip() not in delimiters):
      if category_tree == "":
        category_tree = category_level.strip()
      else:
        category_tree = category_tree +"|" + category_level.strip()
  category_tree = category_tree.replace("||","|")
  #6. Return the result
  return category_tree






#This Section For Writing To Database

def put_into_mysql_database(desc, link, img, price, unit, sitename, category, specs, mycursor, connection):

#TODO handle specs
# def put_into_database():
  print("DESCRIPTION")
  print(desc)
  print("\n\nLINK")
  print(link)
  print("\n\nIMAGE")
  print(img)
  print("\n\nPRICE")
  print(price)
  print("\n\nSITENAME")
  print(sitename)
  print("\n\nCATEGORY")
  print(category)
  print("\n\nUNIT")
  print(str(unit))
  txntime_cd = datetime.datetime.utcnow()
  print("TIME")
  print(txntime_cd)

  #Stuff after the deleted squl code
  print("Trying to write to database")

  try:
    sql = \
      'INSERT INTO  ft_crawled_data (site_name,category,item_description,price,url,image_source,txntime,unit) VALUES (%s, %s,%s, %s,%s,%s,%s,%s)'
    val = (str(sitename), str(category), str(desc), str(price), str(link),str(img),str(txntime_cd),str(unit))
  except:
    print("Sql shit failed")
  try:
    mycursor.execute(sql, val)
  except:
    print("THE execute failed")
  try:
    connection.commit()
  except:
    print("FAILED TO COMMIT")



def put_into_database(desc, link, img, price, sitename, category, unit=""):

  print("DESCRIPTION")
  print(desc)
  print("\n\nLINK")
  print(link)
  print("\n\nIMAGE")
  print(img)
  print("\n\nPRICE")
  print(price)
  print("\n\nSITENAME")
  print(sitename)
  print("\n\nCATEGORY")
  print(category)
  print("\n\nUNIT")
  print(unit)
  txntime_cd = datetime.datetime.utcnow()


  sqlite_file = 'db.sqlite3'
  table_name = 'ft_catalogued_data'
  conn = sqlite3.connect(sqlite_file)
  c = conn.cursor()

  if unit == "":
    c.execute("INSERT INTO ft_catalogued_data(item_description,price,category,url,site_name,image_source,txntime) VALUES (?,?,?,?,?,?,?)",
    (desc,price,category,link,sitename,img,txntime_cd))
    conn.commit()
  else:
    c.execute("INSERT INTO ft_catalogued_data(item_description,price,category,url,site_name,image_source,txntime,unit) VALUES (?,?,?,?,?,?,?,?)",
    (desc,price,category,link,sitename,img,txntime_cd,unit))
    conn.commit()



def put_into_mysql_database_full(desc, link, img, price, sitename, category, unit=""):

# def put_into_database():
  print("DESCRIPTION")
  print(desc)
  print("\n\nLINK")
  print(link)
  print("\n\nIMAGE")
  print(img)
  print("\n\nPRICE")
  print(price)
  print("\n\nSITENAME")
  print(sitename)
  print("\n\nCATEGORY")
  # category = "Name of category"
  print(category)
  print("\n\nUNIT")
  print(str(unit))
  txntime_cd = datetime.datetime.utcnow()
  print("TIME")
  print(txntime_cd)

  # time.sleep(10)

  # time.sleep(10)
  #Local DB Insert
  # sqlite_file = 'db.sqlite3'
  # table_name = 'ft_catalogued_data'
  # conn = sqlite3.connect(sqlite_file)
  # c = conn.cursor()

  # if unit == "":
  #   c.execute("INSERT INTO ft_catalogued_data(item_description,price,category,url,site_name,image_source,txntime) VALUES (?,?,?,?,?,?,?)",
  #   (desc,price,category,link,sitename,img,txntime_cd))
  #   conn.commit()
  # else:
  #   c.execute("INSERT INTO ft_catalogued_data(item_description,price,category,url,site_name,image_source,txntime,unit) VALUES (?,?,?,?,?,?,?,?)",
  #   (desc,price,category,link,sitename,img,txntime_cd,unit))
  #   conn.commit()

  #Deployed DB Insert
# val = (sitename, category, desc, price, link,img,txntime_cd,unit)

  # sitename = "ian"
  # category = "is"
  # desc = "the"
  # price = "best"
  # link = "at"
  # img = "Sql"
  # txntime_cd = "and"
  # unit = "life"

  print("Trying to write to database")
  # time.sleep(10)

  sshtunnel.SSH_TIMEOUT = 550.0
  sshtunnel.TUNNEL_TIMEOUT = 550.0
  # if unit == "":
  #   with sshtunnel.SSHTunnelForwarder('ssh.pythonanywhere.com',
  #                                     ssh_username='iclam19',
  #                                     ssh_password='@astest@1234',
  #                                     remote_bind_address=('iclam19.mysql.pythonanywhere-services.com'
  #                                     , 3306)) as tunnel:
  #       connection = mysql.connector.connect(user='iclam19',
  #               password='astest1234', host='127.0.0.1',
  #               port=tunnel.local_bind_port,
  #               database='iclam19$AssembledSupply')
  #       mycursor = connection.cursor()
  #       sql = \
  #           'INSERT INTO  ft_catalogued_data (site_name,category,item_description,price,url,image_source,txntime) VALUES (%s, %s,%s, %s,%s,%s,%s)'
  #       val = (sitename, category, desc, price, link,img,txntime_cd)
  #       mycursor.execute(sql, val)
  #       connection.commit()
  #       connection.close()
  #       print("IT PRINTED FIRST TRY MR DUDER")
  #       time.sleep(100)

  # else:
  try:
    with sshtunnel.SSHTunnelForwarder('ssh.pythonanywhere.com',
                      ssh_username='iclam19',
                      ssh_password='@astest@1234',
                      remote_bind_address=('iclam19.mysql.pythonanywhere-services.com'
                      , 3306)) as tunnel:
      connection = mysql.connector.connect(user='iclam19',
          password='astest1234', host='127.0.0.1',
          port=tunnel.local_bind_port,
          database='iclam19$AssembledSupply')
      mycursor = connection.cursor()
      sql = \
        'INSERT INTO  ft_crawled_data (site_name,category,item_description,price,url,image_source,txntime,unit) VALUES (%s, %s,%s, %s,%s,%s,%s,%s)'
        # 'INSERT INTO  ft_catalogued_data (site_name,category,item_description,price,url,image_source,txntime,unit) VALUES (%s, %s,%s, %s,%s,%s,%s,%s)'
      # val = (sitename, category, desc, price, link,img,txntime_cd,unit)
      val = (str(sitename), str(category), str(desc), str(price), str(link),str(img),str(txntime_cd),str(unit))
      # val = (test1, test2, test3, test4, test5,test6,test7,test8)
      mycursor.execute(sql, val)
      connection.commit()
      connection.close()
      print("IT PRINTED FIRST TRY MR DUDER")
      # time.sleep(100)
  except:
    Print("You missed a spot")




#This Section For Creating Clients, Browsers, and using Proxies

def new_browser_selenium(browser, element):
  window_before = browser.window_handles[0]
  element.click()
  time.sleep(1)

  ActionChains(browser) \
  .key_down(Keys.CONTROL) \
  .click(add_to_cart) \
  .key_up(Keys.CONTROL) \
  .perform()

  print("There can only be one thing to click")
  time.sleep(2)
  window_after = browser.window_handles[1]
  browser.switch_to_window(window_after)
  print("Im on the second browser")



def selenium_and_soup(url,i="0"):
  print("Using selenium and soup")
  soup = None
  browser = get_selenium_browser()
  try:
    browser.get(url)
  except:
    print(i)
    i = i+1
    selenium_and_soup(url,i)
    if i ==100:
      print("It timed out 101 times")
      time.sleep(90000)
  code = browser.page_source
  soup = BeautifulSoup(code, "html.parser")
  browser.quit()
  return soup

def headless_selenium_and_soup(url):
  soup = None
  browser = get_headless_selenium_browser()
  browser.get(url)
  code = browser.page_source
  soup = BeautifulSoup(code, "html.parser")
  browser.quit()
  return soup



def selenium_and_soup_no_quit(url):
  soup = None
  browser = get_selenium_browser()
  browser.get(url)
  code = browser.page_source
  soup = BeautifulSoup(code, "html.parser")
  return soup


def get_selenium_browser():
  prox = Proxy()
  prox.proxy_type = ProxyType.MANUAL
  proxy_address = get_proxy()
  prox.http_proxy = proxy_address
  prox.socks_proxy = proxy_address
  prox.ssl_proxy = proxy_address

  capabilities = webdriver.DesiredCapabilities.CHROME
  prox.add_to_capabilities(capabilities)
  opts = Options()
  ua = load_user_agent()
  user_agent_arg = "user-agent="+ua
  print(user_agent_arg)
  # time.sleep(100)
  opts.add_argument(user_agent_arg)
  # time.sleep(11100)
  # capabilities =

  browser = webdriver.Chrome(chrome_options=opts, desired_capabilities = capabilities)

  return browser


# def get_selenium_browser():
#   prox = Proxy()
#   prox.proxy_type = ProxyType.MANUAL
#   proxy_address = get_proxy()
#   prox.http_proxy = proxy_address
#   prox.socks_proxy = proxy_address
#   prox.ssl_proxy = proxy_address

#   capabilities = webdriver.DesiredCapabilities.CHROME
#   prox.add_to_capabilities(capabilities)

#   # capabilities =
#   browser = webdriver.Chrome(desired_capabilities = capabilities)

#   return browser


def get_headless_selenium_browser():
  prox = Proxy()
  prox.proxy_type = ProxyType.MANUAL
  proxy_address = get_proxy()
  prox.http_proxy = proxy_address
  prox.socks_proxy = proxy_address
  prox.ssl_proxy = proxy_address


  capabilities = webdriver.DesiredCapabilities.CHROME
  prox.add_to_capabilities(capabilities)

  chrome_options = Options()
  ua = load_user_agent()
  user_agent_arg = "user-agent="+ua
  print(user_agent_arg)

  chrome_options.add_argument(user_agent_arg)
  prefs={"profile.managed_default_content_settings.images": 2, 'disk-cache-size': 4096 }
  chrome_options.add_experimental_option('prefs', prefs)

  chrome_options.add_argument("headless")
  # capabilities =
  browser = webdriver.Chrome(chrome_options=chrome_options,desired_capabilities = capabilities)

  return browser



def get_selenium_browser_random_proxy():
  prox = Proxy()
  prox.proxy_type = ProxyType.MANUAL
  proxy_address = get_random_proxy()
  prox.http_proxy = proxy_address
  prox.socks_proxy = proxy_address
  prox.ssl_proxy = proxy_address

  capabilities = webdriver.DesiredCapabilities.CHROME
  prox.add_to_capabilities(capabilities)

  # capabilities =
  browser = webdriver.Chrome(desired_capabilities = capabilities)
  browser.set_page_load_timeout(1000)
  # driver.Manage().Timeouts().PageLoad = TimeSpan.FromSeconds(10);

  return browser



def get_secure_connection(url):

  code = None
  global proxy
  global user_agent

  print("\nURL")
  print(url)

  for i in range(10):

    session = requests.session()
    session.cookies.clear()

    if(proxy == None and user_agent == None):
      proxy = get_proxy()
      user_agent = load_user_agent()

    print("configuring session . . . ")

    session.proxies['https'] = 'https://astest:assembledtesting123@' + proxy
    session.proxies['http'] = 'http://astest:assembledtesting123@' + proxy

    headers = {
          'Connection' : 'close',
          'user-agent' : user_agent
        }

    try:
      print("requesting page . . .")
      code = session.get(url, headers=headers, timeout=15)
      print("Success!")
      break

    except:
      print("proxy server failed, trying another")
      proxy = None
      user_agent = None
      continue

  return code


def get_random_proxy():

  print("fetching a proxy ip . . . ")

  result_ip = None

  url = "https://www.us-proxy.org/"
  code = requests.get(url, timeout = 30)

  soup = BeautifulSoup(code.text, "html.parser")

  proxy_table = soup.findAll("tbody")

  if(proxy_table == None):
    print("ERROR: The proxy table is empty")
    return

  proxies = proxy_table[0].findAll("tr")

  while(result_ip == None):

    proxy = random.choice(proxies)

    td = proxy.findAll("td")
    type = str(td[4].string)
    https = str(td[6].string)

    if(type == "elite proxy" and https == "yes"):
      ip = str(td[0].string)
      port = str(td[1].string)

      result_ip = ip + ":" + port

      print(result_ip)

  return result_ip




def get_proxy():

  print("fetching a proxy ip . . . ")

  result_ip = random.choice([
  '107.150.89.29:80/',
  '108.174.54.159:80/',
  '154.16.45.82:80/',
  '104.160.10.105:80/',
  '104.160.10.103:80/'])
  print(result_ip)

  return result_ip



def load_user_agent():

  print("fetching a user agent . . . ")

  lines = open('static/user_agents.txt').read().splitlines()
  ua = random.choice(lines)

  print(ua)

  return ua


def sleep_counter(duration):
  for i in range(duration):
    time.sleep(1)
    print(i + 1)

#
# class Client(QWebEnginePage):
#     def __init__(self,url):
#         global app
#         self.app = QApplication(sys.argv)
#         QWebEnginePage.__init__(self)
#         self.html = ""
#         self.loadFinished.connect(self.on_load_finished)
#         self.load(QUrl(url))
#         self.app.exec_()
#
#     def on_load_finished(self):
#         self.html = self.toHtml(self.Callable)
#         print("Load Finished")
#
#     def Callable(self,data):
#         self.html = data
#         self.app.quit()
