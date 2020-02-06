
import generalized_link_crawler as gc
import json
import re



class speedymetals_crawler(gc.Site):

    # return terms of service else None
    def terms_of_service(self):
        pass


    # return robots.txt else None
    def robots_txt(self):
        pass


    # param browser object of the page
    # return a list of categories as browser objects
    def get_cats(self):
        if(self.url == "http://www.speedymetals.com/"):
            return self.soup.select("ul.desktop-menu > li")[:-2]
        else:
            cats = self.soup.select("div.ShapeContainer > div")
            if(len(cats) > 0):
                return cats 
            else:
                return self.soup.select("div.ProductTable > div")[1:]


    # param browser object of a category tag
    # return the name of the category as a string
    def get_cat_name(self, cat):
        if(self.url == "http://www.speedymetals.com/"):
            return cat.select_one("a").text[:-1]
        else:
            try:
                return cat.select("a")[1].text
            except:
                return ""


    # param bs object containing a category
    # return the link for that category
    def get_cat_link(self, cat):
        return self.header + cat.select_one("a")['href']

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
        return self.header + page.select_one("a.toProductClick")['href']


    # return the link of the next page button
    def get_next_page_link(self):
        button = self.soup.select("div.pagenum > a")[-1].select_one("img")
        if(button is not None):
            return self.header + self.soup.select("div.pagenum > a")[-1]['href']
        else:
            return None

    # param browser object of the page
    # return a list of products as browser objects
    def get_prods(self):
        return self.soup.select("div.ProductVariantRow")[1:]

    # param browser object of the item to be scraped
    # return item description as a string
    def get_item_desc(self, item):
        desc = self.soup.select_one("div.ProductNameText > h1").text.strip()
        desc_spec = self.soup.select_one("div.CondensedDarkCellText").text.strip()
        spec = item.select_one("div.ProductVariantRowCellName").text.strip()
        return desc + " " + desc_spec + " " + spec

    # param browser object of the item to be scraped
    # return item link as a string
    def get_item_link(self, item):
        return self.url

    # param browser object of the item to be scraped
    # return item image as a string
    def get_item_image(self, item):
        return self.header + self.soup.select_one("div.ProductImage > div > img")["src"]

    # param browser object of the item to be scraped
    # return item price as a string
    def get_item_price(self, item):
        return item.select_one("div[itemprop = 'price']").text

    # param browser object of the item to be scraped
    # return unit that the item is sold in as string ("box of 10")
    def get_item_unit(self, item):
        return "EA"

    # param browser object of the item being scrapped
    # return all the specs of the item are returned as a string with the format {'key' : 'val'}
    def get_item_specs(self, item=None):
        res = {}
        specs = self.soup.select("div.ProductDescription > body > p")[2:]
        for spec in specs:
            key_val = spec.text.strip()
            key = key_val[:key_val.index(":")].strip()
            val = key_val[key_val.index(":"):][1:].strip()
            res[key] = val
        return json.dumps(res)

