from BhidCrawler import BhidCrawler
from RshughesCrawler import RshughesCrawler
from TannerCrawler import TannerCrawler

class AbstractCrawlerFactory():

    def get_crawler_factory(crawler):
        if("bhid" in crawler):
            return BhidCrawlerFactory()
        elif("rshughes" in crawler):
            return RshughesCrawlerFactory()
        elif("tanner" in crawler):
            return TannerCrawlerFactory()


class BhidCrawlerFactory():

    def __init__(self):
        pass 

    def get_crawler(self):
        return BhidCrawler("https://www.bhid.com/catalog/products", "bhid.com", "https://www.bhid.com/")


class RshughesCrawlerFactory():

    def __init__(self):
        pass 

    def get_crawler(self):
        return RshughesCrawler("https://www.rshughes.com/", "rshughes.com", "https://www.rshughes.com/")

    
class TannerCrawlerFactory():

    def __init__(self):
        pass

    def get_crawler(self):
        return TannerCrawler("https://www.tannerbolt.com/?page=customer&file=customer/tabonu/b2bse/includes/shop.aspx", "tannerbolt.com", "https://www.tannerbolt.com/")


