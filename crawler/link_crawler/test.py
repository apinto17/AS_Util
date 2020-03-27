import sys
sys.path.append('../')
import crawler_util.crawler as c
from bs4 import BeautifulSoup
import production_tool as pt
import generalized_link_crawler as gc 



def main():
    prod_tool = pt.Prod_Tool_Supply("https://www.pts-tools.com", "pts-tools.com", "https://www.pts-tools.com/")
    code = c.get_secure_connection_splash(prod_tool.url, None)
    
    soup = BeautifulSoup(code.text, "html.parser")

    file = open("test.html", "w+")
    file.write(soup.text)


if(__name__ == "__main__"):
    main()

