import generalized_crawler as gc
import bhid_crawler as bh


def main():
    bhid = bh.bhid_crawler("https://www.bhid.com/itemdetail/DIXVAL%20HTBG", "bhid.com", "https://www.bhid.com/")
    gc.crawl_site(bhid)


if(__name__ == "__main__"):
    main()