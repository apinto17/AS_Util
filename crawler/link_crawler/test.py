
from bs4 import BeautifulSoup
import qcsupply_crawler as qc
import generalized_link_crawler as gc


def main():
    qcsupply = qc.qcsupply_crawler("https://www.qcsupply.com/commercial-industrial.html?categories_leaf=Heater+Parts", "qcsupply.com", "https://www.qcsupply.com/")
    qcsupply.follow_url("https://www.qcsupply.com/commercial-industrial.html?categories_leaf=Heater+Parts")
    gc.DFS_on_categories(qcsupply, "")

if(__name__ == "__main__"):
    main()

