
import generalized_link_crawler as gc
import json



class tanner_crawler(gc.Site):

    # return terms of service else None
    def terms_of_service(self):
        pass


    # return robots.txt else None
    def robots_txt(self):
        pass


    # param browser object of the page
    # return a list of categories as browser objects
    def get_cats(self):
        if(self.url == "https://www.tannerbolt.com/"):
            return self.soup.select("ul[id='HeaderProducts'] > li")
        else:
            return self.soup.select("div[id='Categories'] > div.CategoryWrapper")

    # param browser object of a category tag
    # return the name of the category as a string
    def get_cat_name(self, cat):
        if(self.url == "https://www.tannerbolt.com/"):
            return cat.select_one("a").text.strip()
        else:
            return cat.select_one("div.CategoryTitle").text.strip()

    # param bs object containing a category
    # return the link for that category
    def get_cat_link(self, cat):
        if(self.url == "https://www.tannerbolt.com/"):
            return self.header + cat.select_one("a")['href']
        else:
            return self.header + cat.select_one("a.CategoryLink")['href']

    # param browser object of the page
    # return the link to the show all page as a string if it exits
    # else return None
    def get_show_all_page(self):
        return None

    # param browser object of the page
    # return a list of pages of products as browser objects
    # else return None
    def get_prod_pages(self):
        prod_pages = self.soup.select("a.ItemSearchResults_PageLinks")
        res = []
        for page in prod_pages:
            if(self.header + page['href'] not in res):
                res.append(self.header + page['href'])
        return res

    # return the link for the given prod page
    def get_prod_page_link(self, page):
        return self.header + page.select_one("a.ItemDetailsLink")['href']


    # return the link of the next page button
    def get_next_page_link(self):
        return None

    # param browser object of the page
    # return a list of products as browser objects
    def get_prods(self):
        return self.soup.select("div.Product")

    # param browser object of the item to be scraped
    # return item description as a string
    def get_item_desc(self, item):
        return item.select_one("a.ItemDetailsLink > p").text

    # param browser object of the item to be scraped
    # return item link as a string
    def get_item_link(self, item):
        return self.header + item.select_one("a.ItemDetailsLink")['href']

    # param browser object of the item to be scraped
    # return item image as a string
    def get_item_image(self, item):
        return self.header + item.select_one("div.ProductImgWrapper > img")['src']

    # param browser object of the item to be scraped
    # return item price as a string
    def get_item_price(self, item):
        return item.select_one("span.Price").text

    # param browser object of the item to be scraped
    # return unit that the item is sold in as string ("box of 10")
    def get_item_unit(self, item):
        return item.select_one("div.UMWrap > span").text

    # param browser object of the item being scrapped
    # return all the specs of the item are returned as a string with the format {'key' : 'val'}
    def get_item_specs(self, item=None):
        res = {}
        specs = self.soup.select("table.TechSpecs > tbody > tr")
        for spec in specs:
            key = spec.select_one("td.AttrName").text
            val = spec.select_one("td.AttrValue").text
            res[key] = val
        return json.dumps(res)