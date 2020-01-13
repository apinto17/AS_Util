import scrapy
from bs4 import BeautifulSoup
import re
from HarveyNorman.items import HarveyNormanItem

# scrapy shell: "http://localhost:8050/render.html?url=https://www.bhid.com/&timeout=10&wait=0.5"


class HarveyNormanSpider(scrapy.Spider):
    name = 'HarveyNormanspider'
    allowed_domains = ['HarveyNorman.com.au']
    start_urls = ['https://www.HarveyNorman.com.au/']

    def __init__(self):
        self.declare_xpath()

        #All the XPaths the spider needs to know go here
    def declare_xpath(self):
        self.getAllCategoriesXpath = ""
        self.getAllSubCategoriesXpath = ""
        self.getAllItemsXpath = ""
        self.TitleXpath  = ""
        self.CategoryXpath = ""
        self.PriceXpath = ""
        self.FeaturesXpath = ""
        self.DescriptionXpath = ""
        self.SpecsXpath = ""

    def parse(self, response):
        for href in response.xpath(self.getAllCategoriesXpath):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url=url,callback=self.parse_category)
 
    def parse_category(self,response):
        for href in response.xpath(self.getAllSubCategoriesXpath):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url,callback=self.parse_subcategory)

    def parse_subcategory(self,response):
        for href in response.xpath(self.getAllItemsXpath):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url,callback=self.parse_main_item)

    
    def parse_main_item(self,response):
        item = HarveyNormanItem()
 
        Title = response.xpath(self.TitleXpath).extract()
        Title = self.cleanText(self.parseText(self.listToStr(Title)))
 
        Category = response.xpath(self.CategoryXpath).extract()
        Category = self.cleanText(self.parseText(Category))
 
        Price = response.xpath(self.PriceXpath).extract()
        Price = self.cleanText(self.parseText(self.listToStr(Price)))
 
        Features = response.xpath(self.FeaturesXpath).extract()
        Features = self.cleanText(self.parseText(self.listToStr(Features)))
 
        Description = response.xpath(self.DescriptionXpath).extract()
        Description = self.cleanText(self.parseText(self.listToStr(Description)))

        Specs = response.xpath(self.SpecsXpath).extract()
        Specs = self.cleanText(self.parseText(Specs))

        #Put each element into its item attribute.
        item['Title']           = Title
        item['Category']        = Category
        item['Price']           = Price
        item['Features']        = Features
        item['Description']     = Description
        item['Specs']           = Specs
        return item
 
    #Methods to clean and format text to make it easier to work with later
    def listToStr(self,MyList):
        dumm = ""
        MyList = [i.encode('utf-8') for i in MyList]
        for i in MyList:dumm = "{0}{1}".format(dumm,i)
        return dumm
 
    def parseText(self, str):
        soup = BeautifulSoup(str, 'html.parser')
        return re.sub(" +|\n|\r|\t|\0|\x0b|\xa0",' ',soup.get_text()).strip()
 
    def cleanText(self,text):
        soup = BeautifulSoup(text,'html.parser')
        text = soup.get_text()
        text = re.sub("( +|\n|\r|\t|\0|\x0b|\xa0|\xbb|\xab)+",' ',text).strip()
        return text