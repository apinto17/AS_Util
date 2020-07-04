from BhidCrawler import BhidCrawler
from RshughesCrawler import RshughesCrawler
from TannerCrawler import TannerCrawler
from DirectToolsCrawler import DirectToolsCrawler
from HiscoCrawler import HiscoCrawler
from MartinSupplyCrawler import MartinSupplyCrawler
from VallenCrawler import VallenCrawler
from USAIndustrialSupplyCrawler import USAIndustrialSupplyCrawler
from DGISupplyCrawler import DGISupplyCrawler

# TODO add more streamlined registration process

class AbstractCrawlerFactory():

    def get_crawler_factory(crawler):
        if("bhid" in crawler.lower()):
            return BhidCrawlerFactory()
        elif("rshughes" in crawler.lower()):
            return RshughesCrawlerFactory()
        elif("tanner" in crawler.lower()):
            return TannerCrawlerFactory()
        elif("directtools" in crawler.lower()):
            return DirectToolsCrawlerFactory()
        elif("martinsupply" in crawler.lower()):
            return MartinSupplyFactory()
        elif("vallen" in crawler.lower()):
            return VallenCrawlerFactory()
        elif("usa" in crawler.lower()):
            return USAIndustrialSupplyCrawlerFactory()
        elif("dgi" in crawler.lower()):
            return DGISupplyCrawlerFactory()
        elif("hisco" in crawler.lower()):
            return HiscoCrawlerFactory()


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


class DirectToolsCrawlerFactory():

    def __init__(self):
        pass

    def get_crawler(self):
        return DirectToolsCrawler("https://www.directtools.com/category/hardware.html", "www.directtools.com", "https://www.directtools.com/")



class HiscoCrawlerFactory():

    def __init__(self):
        pass

    def get_crawler(self):
        return HiscoCrawler("https://www.hisco.com/product-index", "www.hisco.com", "https://www.hisco.com/")


class MartinSupplyFactory():

    def __init__(self):
        pass

    def get_crawler(self):
        return MartinSupplyCrawler("https://shop.martinsupply.com/store/categoryList.cfm", "www.martinsupply.com", "https://shop.martinsupply.com/")


class VallenCrawlerFactory():

    def __init__(self):
        pass

    def get_crawler(self):
        return VallenCrawler("https://www.vallen.com/categories", "www.vallen.com", "https://www.vallen.com/")


class USAIndustrialSupplyCrawlerFactory():

    def __init__(self):
        pass

    def get_crawler(self):
        return USAIndustrialSupplyCrawler("https://www.usaindustrialsupply.com/index.php", "www.usaindustrialsupply.com", "https://www.usaindustrialsupply.com/")


class DGISupplyCrawlerFactory():

    def __init__(self):
        pass

    def get_crawler(self):
        return DGISupplyCrawler("https://www.dgisupply.com/INTERSHOP/web/WFS/DGISupply-US-Site/en_US/-/USD/ViewShopProducts-Start", "www.dgisupply.com", "https://www.dgisupply.com/")

