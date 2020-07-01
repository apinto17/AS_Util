import sys
sys.path.append('../')

import crawler_util.crawler as c
import MartinSupplyCrawler as mt
import GeneralizedCrawler as gc
import time


def main():
    martin = mt.MartinSupplyCrawler("https://shop.martinsupply.com/store/categoryList.cfm", "www.martinsupply.com", "https://shop.martinsupply.com/")
    gc.DFS_on_categories(martin, "")

if(__name__ == "__main__"):
    main()