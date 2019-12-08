import generalized_link_crawler as gc
import json

class baleigh_crawler(gc.Site):

    # return terms of service else None
    def terms_of_service(self):
        self.follow_url("https://www.baileigh.com/terms-of-sale/")
        return self.soup.select_one("div[class=std]").text


    # return robots.txt else None
    def robots_txt(self):
        self.follow_url("https://www.baileigh.com/robots.txt")
        return self.soup.text

    # return a list of categories as a list of soup objects
    def get_cats(self):
        if(self.url == "https://www.baileigh.com/"):
            res = []
            self.follow_url("https://www.baileigh.com/metalworking")
            res.append(self.soup.select("ol[id=layered-nav-links] > li"))
            self.follow_url("https://www.baileigh.com/woodworking")
            res.append(self.soup.select("ol[id=layered-nav-links] > li"))
            return res
        else:
            return self.soup.select("div.col-main > div.category-listing")


    # param soup object of a category tag
    # return the name of the category as a string
    def get_cat_name(self, cat):
        if(self.url == "https://www.baileigh.com/" or self.url == "https://www.baileigh.com/metalworking" or self.url == "https://www.baileigh.com/woodworking"):
            return cat.select_one("div.parent-header > a").text
        else:
            return cat.select_one("h3").text


    # param bs object containing a category
    # return the link for that category
    def get_cat_link(self, cat):
        if(self.url == "https://www.baileigh.com/" or self.url == "https://www.baileigh.com/metalworking" or self.url == "https://www.baileigh.com/woodworking"):
            return cat.select_one("div.parent-header > a")['href']
        else:
            return cat.select_one("ul > li > a")['href']

    # param browser object of the page
    # return the link to the show all page as a string if it exits
    # else return None
    def get_show_all_page(self):
    	return None

    # param browser object of the page
    # return a list of pages of products as browser objects
    # else return None
    def get_prod_pages(self):
    	return None

    # return the link for the given prod page
    def get_prod_page_link(self, page):
    	return None


    # return the link of the next page button
    def get_next_page_link(self):
        return None


    # return a list of products as soup objects
    def get_prods(self):
        return self.soup.select("ol.products-list > li.item")

    # param soup object of the item to be scraped
    # return item description as a string
    def get_item_desc(self, item):
    	return item.select_one("div[class='desc std']").text.strip()


    # param soup object of the item to be scraped
    # return item link as a string
    def get_item_link(self, item):
    	return item.select_one("div[class='item-cell middle'] > h2.product-name a")['href']


    # param soup object of the item to be scraped
    # return item image as a string
    def get_item_image(self, item):
    	return item.select_one("img")['src']


    # param soup object of the item to be scraped
    # return item price as a string
    def get_item_price(self, item):
        return item.select_one("span.regular-price > span.price").text


    # param soup object of the item to be scraped
    # return unit that the item is sold in as string ("box of 10")
    def get_item_unit(self, item):
        return None



    # param soup object of the item being scrapped
    # return all the specs of the item are returned as a string with the format {'key' : 'val'}
    def get_item_specs(self, item=None):
        res = {}
        specs = self.soup.select("table.product-attribute-specs-table > tbody > tr")
        for spec in specs:
            key = spec.select_one("th.label").text
            val = spec.select_one("td[class='data']").text
            res[key] = val
        return json.dumps(res)





        
