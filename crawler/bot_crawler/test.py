import sys
sys.path.append('../')

import crawler_util.crawler as c
import DirectToolsCrawler as dt
import GeneralizedCrawler as gc
import time


def main():
    direct = dt.DirectToolsCrawler("https://www.directtools.com/category/paint.html", "www.directtools.com", "https://www.directtools.com/")
    gc.DFS_on_categories(direct, "")

if(__name__ == "__main__"):
    main()