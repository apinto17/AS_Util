import requests
from bs4 import BeautifulSoup
import crawler as c


def get_msc_cats(url, cats=""):

    c.sleep_counter(c.SLEEP_TIME)
    print(url)

    soup = c.headless_selenium_and_soup(url)
    if(soup == None):
        return e.NO_SITE_FOUND

    # if you're in a category page
    if(len(soup.findAll("div", {"class": "three wide computer five wide tablet eight wide mobile column center aligned doubleClickHandler"})) > 0):
        DFS_on_categories(soup, cats)
    # if you're on a product page
    else:
        print(cats)


# depth first search starting on the first category
def DFS_on_categories(soup, cats):

    for cat in soup.findAll("div", {"class": "three wide computer five wide tablet eight wide mobile column center aligned doubleClickHandler"}):
        cat_name = cat.find("h3", {"class" : "ui header"}).string
        cat_name = cats + cat_name.strip(" \n\t")
        cat_link = cat.find("a")['href']
        get_msc_cats("https://www.mscdirect.com" + cat_link, cat_name + "|")


if(__name__ == "__main__"):
	get_msc_cats("https://www.mscdirect.com/ProductsHomeView")
