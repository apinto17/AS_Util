import sys
sys.path.append('../')

import crawler_util.crawler as c
import BhidCrawler as bh
import GeneralizedCrawler as gc
import time


def main():
    bhid = bh.BhidCrawler("https://www.bhid.com/catalog/products", "bhid.com", "https://www.bhid.com/")
    bhid.browser = c.get_selenium_browser()
    bhid.follow_url(bhid.url)
    cats = bhid.get_cats()
    bhid.browser.execute_script("""
                                var rect = arguments[0].getBoundingClientRect();
                                window.scrollTo(0, rect.top);
                                """, cats[0])
    time.sleep(1)
    print(bhid.get_cat_name(cats[0]))
    cats[0].click()




if(__name__ == "__main__"):
    main()