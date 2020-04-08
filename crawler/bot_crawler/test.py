import sys
sys.path.append('../')
from bs4 import BeautifulSoup
import crawler_util.crawler as c
import time


def main():
    browser = c.get_headless_selenium_browser()
    browser.get("https://www.rshughes.com/c/Abrasive-Brush-Accessories/1096/")
    soup = BeautifulSoup(browser.page_source, "html.parser")
    elem = soup.select_one("span.x-spec-name")
    print("HERE")
    print(elem.text)
    print("HERE")


if(__name__ == "__main__"):
    main()