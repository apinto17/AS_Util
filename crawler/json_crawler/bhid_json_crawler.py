
import sys
sys.path.append('../')
import json
import crawler_util.crawler as c
from crawler_util.server import Server
import multiprocessing as mp
import math

NUM_PROCESSES = 5



def crawl():
    categories = get_json("https://www.bhid.com/api/v1/categories")
    categories = categories["categories"][0]["subCategories"][1:]
    cat_ranges = gen_cat_ranges(categories)

    # split processes and crawl
    p = mp.Pool(NUM_PROCESSES)

    p.map(DFS_on_category_range, cat_ranges)
    p.terminate()
    p.join()


def gen_cat_ranges(categories):
    ranges = []
    cat_adder = math.floor(len(categories) / NUM_PROCESSES)
    start = 0
    end = start + cat_adder
    for i in range(NUM_PROCESSES):
        ranges.append(categories[start:end])
        start += cat_adder
        end += cat_adder
    
    return ranges




def DFS_on_category_range(categories):
    for i in range(len(categories)):
        cats = categories[i]["name"]
        DFS_on_categories(categories[i]["path"], cats)


def DFS_on_categories(category, cats, server=None):
    print(cats)
    # server = Server()
    # server.connect()
    json_resp = get_json("https://www.bhid.com/api/v1/catalogpages?path=" + category)
    categories = json_resp["category"]["subCategories"]
    if(len(categories) > 0):
        for i in range(len(categories)):
            old_cats = cats
            cats += "|" + categories[i]["name"]
            DFS_on_categories(categories[i]["path"], cats, server)
            cats = old_cats
    else:
        get_products(cats, json_resp["category"]["id"], server)
        

def get_products(cats, cat_id, server):
    product_json = get_json("https://www.bhid.com/api/v1/products?page=1&categoryId=" + cat_id)
    while(True):
        products = product_json["products"]
        for prod in products:
            get_product(prod["id"], cats, server)

        next_page = product_json["pagination"]["nextPageUri"]
        if(next_page is None):
            break
        else:
            product_json = get_json(next_page)



def get_product(product_id, cats, server):
    product = get_json("https://www.bhid.com/api/v1/products/" + product_id + "?expand=documents,specifications,styledproducts,htmlcontent,attributes,,pricing,brand&includeAttributes=IncludeOnProduct")
    desc = product["product"]["shortDescription"]
    price = get_price(product)
    link = "https://www.bhid.com/" + product["product"]["productDetailUrl"]
    img = product["product"]["smallImagePath"]
    unit = product["product"]["unitOfMeasure"]
    sitename = "bhid.com"
    specs = json.dumps(get_specs(product))
    print("---------------------------------")
    print(desc)
    if(price is not None):
    #    server.write_to_db(desc, link, img, price, unit, sitename, cats, specs)
    


def get_specs(product):
    res = {}
    specs = product["product"]["attributeTypes"]
    for spec in specs:
        res[spec["name"]] = get_spec_values(spec)

    return res


def get_spec_values(spec):
    res = []
    for val in spec["attributeValues"]:
        res.append(val["value"])
    if(len(res) == 1):
        return res[0]
    else:
        return res 



def get_price(product):
    url = "https://www.bhid.com" + product["product"]["productDetailUrl"]
    browser = c.get_headless_selenium_browser()
    browser.get(url)
    c.sleep_counter(3)
    try:
        price = browser.find_element_by_css_selector("span.unit-net-price").text
    except:
        return None
    if(price == "Request Price"):
        return None
    return price


def get_json(url):
    c.sleep_counter(c.SLEEP_TIME)
    categories = c.get_secure_connection(url).text
    categories = json.loads(categories)
    return categories



if(__name__ == "__main__"):
    crawl()