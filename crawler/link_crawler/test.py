import crawler as c
from bs4 import BeautifulSoup


def main():
    url = "https://www.rshughes.com/"
    code = c.get_secure_connection(url)
    soup = BeautifulSoup(code.text, "html.parser")

    elements = soup.select("ul.nav-l1 > li > a")
    print(len(elements))

if(__name__ == "__main__"):
    main()
