
from bs4 import BeautifulSoup
import kele as k
import generalized_link_crawler as gc


def main():
    kele = k.kele_crawler("https://www.kele.com/product-categories.aspx", "kele.com", "https://www.kele.com/")
    kele.follow_url("https://www.kele.com/product-categories.aspx")
    cats = kele.get_cats()
    for cat in cats:
        print(k.kele_crawler.get_cat_name(cat))

    # CSS selectors
    # beautiful soup selectors

if(__name__ == "__main__"):
    main()

