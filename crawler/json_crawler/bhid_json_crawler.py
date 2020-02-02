
import sys
sys.path.append('../')
import json
import crawler_util.crawler as c
from crawler_util.server import Server
import multiprocessing as mp
import math
import csv
import time
from bs4 import BeautifulSoup
import requests

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
    specs = get_specs(product)
    print("---------------------------------")
    print(desc)
    if(price is not None):
        fields=[desc, price, link, img, unit, sitename, cats, specs]
        with open(r'data_test.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(fields)
        # server.write_to_db(desc, link, img, price, unit, sitename, cats, specs)
    


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
    code = c.get_secure_connection_splash(url)
    soup = BeautifulSoup(code.text, "html.parser")
    price = None
    counter = 0
    for i in range(10):
        try:
            time.sleep(c.SLEEP_TIME / 2)
            price = soup.select_one("span.unit-net-price").text
            print(price)
            break
        except:
            pass
    if(price == "Request Price"):
        return None
    return price


def get_json(url):
    c.sleep_counter(c.SLEEP_TIME)
    categories = c.get_secure_connection(url).text
    categories = json.loads(categories)
    return categories

#TODO maybe try aquarium w/o proxies?

if(__name__ == "__main__"):
    data = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Content-Length": "117",
        "Content-Type": "application/json;charset=UTF-8",
        "Cookie": "_ga=GA1.2.1310733079.1553663560; .ASPXANONYMOUS=4EbbbcrsIE3JGwYTxrh7s_TYu-vGAZ0lUMvrUEtOQtQ5vO62-t_8yUdyhg6eU2Jxoqfh3cZqqnHGDXGtu127tPMbqWW5Uxt7CLaYJmnixMLl-Kj5DXvtNWW0RDF0u3MWb-Tg4g2; CurrentLanguageId=a26095ef-c714-e311-ba31-d43d7e4e88b2; SetContextLanguageCode=en-us; SetContextPersonaIds=d06988c0-9358-4dbb-aa3d-b7be5b6a7fd9; InsiteCacheId=124fbcde-1eb0-422e-a472-9aa02648d4b6; CurrentCurrencyId=30b432b9-a104-e511-96f5-ac9e17867f77; CurrentFulfillmentMethod=Ship; FirstPage=false; RecentlyViewedProducts=%5b%7b%22Key%22%3a%22DIXVAL+4PSG%22%2c%22Value%22%3a%222020-02-02T15%3a22%3a06.319249-06%3a00%22%7d%2c%7b%22Key%22%3a%223M+05114120616%22%2c%22Value%22%3a%222020-01-29T19%3a17%3a06.5455193-06%3a00%22%7d%2c%7b%22Key%22%3a%223M+05114120885%22%2c%22Value%22%3a%222020-01-29T19%3a15%3a05.6075771-06%3a00%22%7d%2c%7b%22Key%22%3a%223M+05114485731%22%2c%22Value%22%3a%222020-01-29T18%3a19%3a50.9293644-06%3a00%22%7d%2c%7b%22Key%22%3a%22CLECO+46606116%22%2c%22Value%22%3a%222020-01-27T17%3a59%3a10.5625115-06%3a00%22%7d%2c%7b%22Key%22%3a%22KYOIND+TJP05256%22%2c%22Value%22%3a%222020-01-27T17%3a57%3a51.4841364-06%3a00%22%7d%2c%7b%22Key%22%3a%22KYOIND+TJP05170%22%2c%22Value%22%3a%222020-01-26T14%3a16%3a30.2501539-06%3a00%22%7d%2c%7b%22Key%22%3a%22REGCUT+017209AW%22%2c%22Value%22%3a%222020-01-26T14%3a15%3a19.8285604-06%3a00%22%7d%5d",
        "Host": "www.bhid.com",
        "Origin": "https://www.bhid.com",
        "Referer": "https://www.bhid.com/catalog/products/measuring-and-inspecting/liquid-flow-measuring-instruments/flow-sight-and-sight-glasses-accessories/dixval-spc-4psg",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"

    }
    code = requests.post('https://www.bhid.com/api/v1/realtimepricing', headers=data)
    # code = json.loads(code.text)
    print(code)


