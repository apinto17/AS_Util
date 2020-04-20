import sys
sys.path.append('../')

import crawler_util.crawler as c
import RshughesCrawler as rs
import GeneralizedCrawler as gc
import time


def main():
    rshughes = rs.RshughesCrawler("https://www.rshughes.com/c/Buffers-And-Polishers/1209204/", "rshughes.com", "https://www.rshughes.com/")
    gc.DFS_on_categories(rshughes, "")

if(__name__ == "__main__"):
    main()