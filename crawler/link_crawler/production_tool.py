

import generalized_link_crawler as gc
import json
import re



class Prod_Tool_Supply(gc.Site):


    # return terms of service else None    
    def terms_of_service(self):
        return None


    # return robots.txt else None   
    def robots_txt(self):
        return None


    # param browser object of the page
    # return a list of categories as browser objects
    def get_cats(self):
        if(self.url == "https://www.pts-tools.com/"):
            return self.soup.select("div.groupItem")
        else:
            return self.soup.select("div.level1_wrapper")


    # param browser object of a category tag
    # return the name of the category as a string   
    def get_cat_name(self, cat):
    	return cat.select_one("div.level1_title > a").text.strip()

    # param bs object containing a category
    # return the link for that category
    
    def get_cat_link(self, cat):
    	return self.header + cat.select_one("div.level1_title > a")['href']

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
        if(self.soup.select_one("#catalog_multiple_selector_products > div.first > div > dir-pagination-controls > ul > li:nth-child(11) > a") is None):
            return None

        script = """
            function main(splash)
                splash.private_mode_enabled = false
                local url = splash.args.url
                assert(splash:go(url)
                splash:select('#catalog_multiple_selector_products > div.first > div > dir-pagination-controls > ul > li:nth-child(11) > a'):mouse_click()
                splash:wait(1)
                return {
                    splash:html()
                }

            end
        """

        return (self.url, script)


    # param browser object of the page
    # return a list of products as browser objects
    
    def get_prods(self):
    	return self.soup.select("li.product.family")

    # param browser object of the item to be scraped
    # return item description as a string
    
    def get_item_desc(self, item):
    	return item.select("div.FamilySD.ng-binding")

    # param browser object of the item to be scraped
    # return item link as a string
    
    def get_item_link(self, item):
    	return self.header + item.select_one("a.compare_product_link")['href']

    # param browser object of the item to be scraped
    # return item image as a string
    
    def get_item_image(self, item):
    	return item.select_one("img")['src']

    # param browser object of the item to be scraped
    # return item price as a string
    
    def get_item_price(self, item):
    	return item.select_one("span.price_number.ng-binding.ng-scope").text

    # param browser object of the item to be scraped
    # return unit that the item is sold in as string ("box of 10")
    
    def get_item_unit(self, item):
    	return item.select_one("span.field_value").text

    # param browser object of the item being scrapped
    # return all the specs of the item are returned as a string with the format {'key' : 'val'}
    
    def get_item_specs(self, item):
        specs = self.soup.select_one("#product_technical_info > tbody > tr")
        res = {}
        for spec in specs:
            key = spec.select_one("td.field_name").text 
            val = spec.select_one("td.field_data").text

            res[key] = val

        return json.dumps(res)


