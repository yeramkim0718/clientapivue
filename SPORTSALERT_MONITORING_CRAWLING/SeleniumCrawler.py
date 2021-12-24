from selenium import webdriver
from bs4 import BeautifulSoup
import re
from enum import IntEnum
import sys
import io
from selenium.common.exceptions import StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

class SeleniumCrawler :
    class Driver(IntEnum) :
        CHROME = 0

    CHROME_PATH ='./Configuration/chromedriver'

    def __init__(self, browser) :
        self.browser = browser
        self.urls = None
        self.driver = None
        self.options = None

    #prefs(dic), arguments(list)
    def set_options(self, prefs, arguments) :
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option('prefs',prefs)
        for argument in arguments :
            self.options.add_argument(argument)
 
        return self.options
    
    def load_webdriver(self) :
        if(self.browser == SeleniumCrawler.Driver.CHROME) :
            driver_path = SeleniumCrawler.CHROME_PATH
            #self.driver = None

            if self.options is not None :
                #self.driver = webdriver.Chrome(driver_path, options=self.options)
                self.driver = webdriver.Chrome(ChromeDriverManager().install(),options = self.options)
            else :
                #self.driver = webdriver.Chrome(driver_path)
                self.driver = webdriver.Chrome(ChromeDriverManager().install())
            self.driver.implicitly_wait(3)

    def quit_webdriver(self) :
        self.driver.quit()       

    def set_urls(self, urls) :
        self.urls = urls

    def check_result (self, result) :
        for unit in result :
            if len(unit) != 0 :
                return True
        return False

    def parse (self, html,parser, tags) :
        
        soup = BeautifulSoup(html, parser)

        result = []
        for tag in tags :
            list = soup.select(tag)
            txts = []
            for li in list :
                txt = li.get_text().replace("\xa0","")
                txts.append(txt)
            result.append(txts)

        """if self.check_result(result) is False :
            result = self.parse(parser,tags)
        """ 
        return result

    def crawleAndParse(self,parser,tags) :

        self.result = []
        self.load_webdriver()

        for i, url in enumerate(self.urls) :
            self.driver.get(url)
            html = self.driver.page_source
            result = self.parse(html,parser,tags[i])
            self.result.append(result)    
            
        self.quit_webdriver()
        return self.result

#TEST CODE
"""
crawler = SeleniumCrawler(SeleniumCrawler.Driver.CHROME)
urls = ['https://www.flashscore.com/american-football/usa/nfl/standings/']
crawler.set_urls(urls)
tags = [['div.rowCellParticipant___3wGbPLz']]
results = crawler.crawleAndParse('html.parser',tags)
print(results)
"""
"""
driver_path = SeleniumCrawler.CHROME_PATH
driver = webdriver.Chrome(driver_path)
driver.implicitly_wait(3)

url = 'https://www.flashscore.com/football/france/ligue-1/results/'
driver.get(url) 
html = driver.page_source
driver.quit()
soup = BeautifulSoup(html, 'html.parser')

tag = 'div.event__part '
list = soup.select(tag)

for one in list :
    print(one.get_text())

"""