
import requests
from bs4 import BeautifulSoup
import crawler as c
import mysql.connector
from mysql.connector import Error
import datetime
import sshtunnel


cur = None
conn = None
first = True

def get_grainger_cats(url, cats=""):

    c.sleep_counter(c.SLEEP_TIME)
    print(url)

    soup = c.headless_selenium_and_soup(url)
    if(soup == None):
        return e.NO_SITE_FOUND

    # if you're in a category page
    if(len(soup.findAll("li", {"class": "list-item"})) > 0):
        DFS_on_categories(soup, cats)
    # if you're on a product page
    else:
        write_to_database(cats)


# depth first search starting on the first category
def DFS_on_categories(soup, cats):

    global first
    if(first):
        first = False
        for cat in soup.findAll("li", {"class": "list-item"})[18:]:
            cat_name = cat.find("span", {"class" : "category-text"}).string
            cat_name = cats + "|" + cat_name.strip(" \n\t")
            cat_link = cat.find("a", {"class" : "route category-link"})['href']
            get_grainger_cats("https://www.grainger.com" + cat_link, cat_name)
    else:
        for cat in soup.findAll("li", {"class": "list-item"}):
            cat_name = cat.find("span", {"class" : "category-text"}).string
            cat_name = cats + "|" + cat_name.strip(" \n\t")
            cat_link = cat.find("a", {"class" : "route category-link"})['href']
            get_grainger_cats("https://www.grainger.com" + cat_link, cat_name)

def write_to_database(cats):
    site_name_variable = 'Grainger'
    input_categories_variable = cats[1:cats.rfind("|")]
    output_category_variable = cats[cats.rfind("|") + 1:]
    print(input_categories_variable)
    print(output_category_variable)


    val = (str(site_name_variable), str(input_categories_variable),str(output_category_variable))

    sql_insert_query = 'INSERT INTO output_category (site_name,input_categories,output_category) VALUES (%s,%s,%s)'
    cur.execute(sql_insert_query,val)
    conn.commit()


def connect():

    global cur
    global conn
    try:
        conn = mysql.connector.connect(host='localhost',
                                       database='as_categories',
                                       user='root',
                                       password='pintosql')

        if conn.is_connected():
            print('Connected to MySQL database')
            cur = conn.cursor()

        else:
            print("Did not connect")

    except Error as e:
        print(e)

if(__name__ == "__main__"):
    connect()
    get_grainger_cats("https://www.grainger.com/category?analytics=nav")
    cur.close()
