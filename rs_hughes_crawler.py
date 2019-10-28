import generalized_crawler as gc
import json

class rs_hughes_crawler(gc.Site):

    def get_cats(self, browser):
        if(self.url == "https://www.rshughes.com/"):
            return browser.find_elements_by_css_selector("ul.nav-l1 > li > a")
        else:
            return browser.find_elements_by_css_selector("tr.x-category-list > td")

    # param browser object of a category tag
    # return the name of the category as a string
    def get_cat_name(self, cat):
        if(self.url == "https://www.rshughes.com/"):
            return cat.find_element_by_css_selector("a > span").text
        else:
            return cat.find_element_by_css_selector("div.category-iconic-name").text

    # param browser object of the page
    # return the link to the show all page as a string if it exits
    # else return None
    def get_show_all_page(self, browser):
    	return None

    # param browser object of the page
    # return a list of pages of products as browser objects
    # else return None
    def get_prod_pages(self, browser):
    	return None

    # param browser object of the page
    # return the next page of products as a browser object
    # else return None
    def get_next_page(self, browser):
        return browser.find_element_by_css_selector("div.nav-overflow > a:last-child")

    # param browser object of the page
    # return a list of products as browser objects
    def get_prods(self, browser):
    	return browser.find_elements_by_css_selector("form.x-product")

    # param browser object of the item to be scraped
    # return item description as a string
    def get_item_desc(self, item):
    	return item.find_element_by_css_selector("a.x-link-name").text

    # param browser object of the item to be scraped
    # return item link as a string
    def get_item_link(self, item):
    	return item.find_element_by_css_selector("a").get_attribute("href")

    # param browser object of the item to be scraped
    # return item image as a string
    def get_item_image(self, item):
    	return item.find_element_by_css_selector("img").get_attribute("src")

    # param browser object of the item to be scraped
    # return item price as a string
    def get_item_price(self, item):
    	return item.find_element_by_css_selector("span.x-price").text

    # param browser object of the item to be scraped
    # return unit that the item is sold in as string ("box of 10")
    def get_item_unit(self, item):
    	return None

    # param browser object of the item being scrapped
    # return all the specs of the item are returned as a string with the format {'key' : 'val'}
    def get_item_specs(self, item):
        res = {}
        specs = item.find_elements_by_css_selector("li.x-spec")
        for spec in specs:
            key = spec.find_element_by_css_selector("span.x-spec-name").text.replace(":", "")
            val = spec.find_element_by_css_selector("span.x-spec-value").text
            res[key] = val
        return json.dumps(res)
