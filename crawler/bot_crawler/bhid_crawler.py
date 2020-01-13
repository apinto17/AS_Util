import generalized_crawler as gc
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
        if(self.browser.current_url == "https://www.bhid.com/"):
            return self.browser.find_elements_by_css_selector("ul[class='sitemap collapse navbar-collapse navbar-wp mega-menu right'] > li")
        else:
            return self.browser.find_elements_by_css_selector("ul[class='categorycontent-container list-unstyled'] > li")


    # param browser object of a category tag
    # return the name of the category as a string
    def get_cat_name(self, cat):
    	return cat.xpath("@text").getall()[:cat.text.index("(")].strip()

    # param browser object of the page
    # return the link to the show all page as a string if it exits
    # else return None
    def get_show_all_page(self):
    	pass

    # param browser object of the page
    # return a list of pages of products as browser objects
    # else return None
    def get_prod_pages(self):
    	pass

    # param browser object of the page
    # return the next page of products as a browser object
    # else return None
    def get_next_page(self):
        next_button = self.browser.find_elements_by_css_selector("div.SearchResultPaging > a")[-1]
        if("NEXT" in next_button.text):
            return next_button 
        else:
            return None

    # param browser object of the page
    # return a list of products as browser objects
    def get_prods(self):
    	return self.browser.find_elements_by_css_selector("div.ng-scope > div")

    # param browser object of the item to be scraped
    # return item description as a string
    def get_item_desc(self, item):
    	return item.find_element_by_css_selector("div.SKULineDescInfo > h2 > a").text.strip()

    # param browser object of the item to be scraped
    # return item link as a string
    def get_item_link(self, item):
    	return item.find_element_by_css_selector("div.SKULineDescInfo > h2 > a").get_attribute("href")

    # param browser object of the item to be scraped
    # return item image as a string
    def get_item_image(self, item):
        img = None
        try:
            img = item.find_element_by_css_selector("div.sku-image-enlarge > a").get_attribute("href")
        except:
            pass 
        return img

    # param browser object of the item to be scraped
    # return item price as a string
    def get_item_price(self, item):
    	return item.find_element_by_css_selector("span.PriceBreaks").text

    # param browser object of the item to be scraped
    # return unit that the item is sold in as string ("box of 10")
    def get_item_unit(self, item):
        unit = None
        try:
            unit = item.find_element_by_css_selector("span.SKULineUOM").get_attribute("data-uom")
        except:
            pass 
        return unit

    # param browser object of the item being scrapped
    # return all the specs of the item are returned as a string with the format {'key' : 'val'}
    def get_item_specs(self, item=None):
        res = {}
        specs = response.css("div.item-specs > ul > li")
        for spec in specs:
            key = spec.css("label::text").get()[:-2]
            val = specs[0].css("div.itemSpecValues::text").get()
            res[key] = val
        return json.dumps(res)