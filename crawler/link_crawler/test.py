import crawler as c
from bs4 import BeautifulSoup


def main():
    url = "https://www.bhid.com/"
    code = c.get_secure_connection(url)
    soup = BeautifulSoup(code.text, "html.parser")

    elements = soup.select("ul[class='sitemap collapse navbar-collapse navbar-wp mega-menu right'] > li")
    print(elements)

if(__name__ == "__main__"):
    main()
