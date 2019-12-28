import generalized_link_crawler as gc
import json

class bhid_crawler(gc.Site):

    # return terms of service else None
    def terms_of_service(self):
        return None


    # return robots.txt else None
    def robots_txt(self):
        return None

    # return a list of categories as a list of soup objects
    def get_cats(self):
        if(self.url == "https://www.bhid.com/"):
            return self.soup.select("div[class='category-flyout-callback']")
        else:
            return self.soup.select("ul[class='categorycontent-container list-unstyled'] > li")


    # param soup object of a category tag
    # return the name of the category as a string
    def get_cat_name(self, cat):
        if(self.url == "https://www.rshughes.com/"):
            return cat.select_one("a > span").text
        else:
            return cat.select_one("div.category-iconic-name").text


    # param bs object containing a category
    # return the link for that category
    def get_cat_link(self, cat):
        if(self.url == "https://www.rshughes.com/"):
            return self.header + cat['href']
        else:
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
    	return None


    # return the link of the next page button
    def get_next_page_link(self):
        return self.soup.select_one("a[title='Next Page']")['href']


    # return a list of products as soup objects
    def get_prods(self):
        return self.soup.select("div[class='x-products x-view-grid'] > form.x-product")

    # param soup object of the item to be scraped
    # return item description as a string
    def get_item_desc(self, item):
    	return item.select_one("a.x-link-name").text

    # param soup object of the item to be scraped
    # return item link as a string
    def get_item_link(self, item):
    	return self.header + item.select_one("a.x-link-name")['href']

    # param soup object of the item to be scraped
    # return item image as a string
    def get_item_image(self, item):
    	return item.select_one("img")['src']

    # param soup object of the item to be scraped
    # return item price as a string
    def get_item_price(self, item):
        price_str = item.select_one("span.x-price").text
        return price_str.split(" ")[0]



    # param soup object of the item to be scraped
    # return unit that the item is sold in as string ("box of 10")
    def get_item_unit(self, item):
        price_str = item.select_one("span.x-price").text
        return price_str.split(" ")[2]



    # param soup object of the item being scrapped
    # return all the specs of the item are returned as a string with the format {'key' : 'val'}
    def get_item_specs(self, item=None):
        res = {}
        specs = item.select("li.x-spec")
        for spec in specs:
            key = spec.select_one("span.x-spec-name").text.replace(":", "")
            val = spec.select_one("span.x-spec-value").text
            res[key] = val
        return json.dumps(res)
