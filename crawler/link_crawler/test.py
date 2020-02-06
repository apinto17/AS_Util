
from bs4 import BeautifulSoup
import bhid_crawler as bh
import generalized_link_crawler as gc 


def main():
    bhid_crawler = bh.bhid_crawler("https://www.bhid.com/catalog/products", "bhid.com", "https://www.bhid.com/")
    bhid_crawler.follow_url(bhid_crawler.url)
    cats = bhid_crawler.get_cats()
    print(len(cats))


if(__name__ == "__main__"):
    main()

