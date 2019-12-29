
from bs4 import BeautifulSoup
import baleigh_indust as bi
import generalized_link_crawler as glc


def main():
    baleigh = bi.baleigh_crawler("www.https://www.baileigh.com/", "baileigh.com", "https://www.baileigh.com/")
    baleigh.follow_url("https://www.baileigh.com/")
    
    glc.DFS_on_categories(baleigh, "")

if(__name__ == "__main__"):
    main()
