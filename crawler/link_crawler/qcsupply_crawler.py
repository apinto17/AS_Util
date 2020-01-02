
import generalized_link_crawler as gc
import json
import re



class qcsupply_crawler(gc.Site):

    # return terms of service else None
    def terms_of_service(self):
        pass


    # return robots.txt else None
    def robots_txt(self):
        pass


    # param browser object of the page
    # return a list of categories as browser objects
    def get_cats(self):
        return self.soup.select("div[class='filter-options-content categories_leaf'] > ol.items > li")

    # param browser object of a category tag
    # return the name of the category as a string
    def get_cat_name(self, cat):
        return cat.select_one("span.filter-item-label").text

    # param bs object containing a category
    # return the link for that category
    def get_cat_link(self, cat):
        return cat.select_one("a")['href']

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
        return page.select_one("a")['href']


    # return the link of the next page button
    def get_next_page_link(self):
        return self.soup.select("ul[class='items pages-items'] > li")[-1].select_one("a")['href']

    # param browser object of the page
    # return a list of products as browser objects
    def get_prods(self):
        return self.soup.select("ol[class='products list items product-items clearer'] > li")

    # param browser object of the item to be scraped
    # return item description as a string
    def get_item_desc(self, item):
        return item.select_one("a.product-item-link").text.strip()

    # param browser object of the item to be scraped
    # return item link as a string
    def get_item_link(self, item):
        return item.select_one("a.product-item-link")['href']

    # param browser object of the item to be scraped
    # return item image as a string
    def get_item_image(self, item):
        return item.select_one("img[class='product-image-photo lazy owl-lazy']")["src"]

    # param browser object of the item to be scraped
    # return item price as a string
    def get_item_price(self, item):
        return item.select_one("span.price").text

    # param browser object of the item to be scraped
    # return unit that the item is sold in as string ("box of 10")
    def get_item_unit(self, item):
        return None

    # param browser object of the item being scrapped
    # return all the specs of the item are returned as a string with the format {'key' : 'val'}
    def get_item_specs(self, item=None):

        if(self.has_spec()):
            res = {}
            for i in range(2):
                try:
                    specs = self.soup.select("div.value > ul")[i].select("li")
                    for spec in specs:
                        key_val = spec.text.strip()
                        key = key_val[:key_val.index(":")].strip()
                        val = key_val[key_val.index(":"):][1:].strip()
                        res[key] = val
                    return json.dumps(res)
                except:
                    pass

        else:
            return None


    def has_spec(self):
        if(self.soup.find("strong", text=re.compile(".*Specifications.*")) is not None):
            return True 
        else:
            return False