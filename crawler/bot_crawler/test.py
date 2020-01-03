import sys
sys.path.append('../')

import crawler_util.crawler as c
import bhid_crawler as bh
import generalized_crawler as gc


def main():
    bhid = bh.bhid_crawler("https://www.bhid.com/", "bhid.com", "https://www.bhid.com/")
    bhid.browser = c.get_headless_selenium_browser()
    gc.DFS_on_categories(bhid, "", 0, 6)




if(__name__ == "__main__"):
    main()