import crawler as c
from bs4 import BeautifulSoup
import rs_hughes_crawler as rsh
import generalized_link_crawler as glc


def main():
    rshughes = rsh.rs_hughes_crawler("https://www.rshughes.com/", "rshughes.com", "https://www.rshughes.com/")
    rshughes.follow_url("https://www.rshughes.com/c/Water-Filters/9702/")
    

    glc.DFS_on_categories(rshughes, "")

if(__name__ == "__main__"):
    main()
