import crawler as c
from bs4 import BeautifulSoup
import rs_hughes_crawler as rsh
import generalized_link_crawler as glc


def main():
    rshughes = rsh.rs_hughes_crawler("https://www.rshughes.com/", "rshughes.com", "https://www.rshughes.com/")
    rshughes.follow_url("https://www.rshughes.com/c/Fixed-Systems/8503/?start_item=73")
    

    elements = rshughes.get_prods()
    print(str(elements[0]))

if(__name__ == "__main__"):
    main()
