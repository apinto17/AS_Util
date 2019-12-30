
from bs4 import BeautifulSoup
import tanner_crawler as t
import generalized_link_crawler as gc


def main():
    tanner = t.tanner_crawler("https://www.tannerbolt.com/products/FASTENERS/BOLTS/04.%20HEX%20HEAD%20CAP%20SCREWS%20PLATED/01.%20HEX%20GRADE%202%20ZINC%20PLATED/01.%20COARSE%20THREAD/01.%2014-20%20GRADE%202.aspx", "tanner.com", "https://www.tannerbolt.com/")
    tanner.follow_url("https://www.tannerbolt.com/products/FASTENERS/BOLTS/04.%20HEX%20HEAD%20CAP%20SCREWS%20PLATED/01.%20HEX%20GRADE%202%20ZINC%20PLATED/01.%20COARSE%20THREAD/01.%2014-20%20GRADE%202.aspx")
    
    gc.DFS_on_categories(tanner, "")

if(__name__ == "__main__"):
    main()
