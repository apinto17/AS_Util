
from bs4 import BeautifulSoup
import speedymetals_crawler as sp
import generalized_link_crawler as gc


def main():
    speedymetals = sp.speedymetals_crawler("http://www.speedymetals.com/", "speedymetals.com", "http://www.speedymetals.com/")
    speedymetals.follow_url("http://www.speedymetals.com/")
    gc.DFS_on_categories(speedymetals, "")

if(__name__ == "__main__"):
    main()

