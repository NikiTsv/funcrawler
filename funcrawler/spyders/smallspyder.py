from spyders.spyder import Spyder
from bs4 import BeautifulSoup
from models.postmodel import PostModel
from models.content import Content
from selenium.webdriver.common.keys import Keys
import time

class SmallSpyder(Spyder):

    name = 'SmallSpyder'

    def __init__(self, website):
        self.website = website

    ###returns content###
    def crawl_content(self):
        print(self.name + " " + self.spyder_reports.initializing())
        driver = self.get_configured_driver()
        print(self.spyder_reports.opening_website())
        driver.get(self.website)
        print(self.spyder_reports.scraping_data())
        scrapes = self.__scrape_content(driver.page_source, driver)
        driver.quit()
        return scrapes

    def __scrape_content(self, source, driver):
        soup = BeautifulSoup(source, "html.parser")
        source = driver.execute_script("return document.body.getElementsByTagName('source');")
        try:
           video = soup.find('video')
           thumbnail = video.get('poster')
           source = soup.findAll('source')
           src = source.get('src')
           content = Content('video/mp4', src, thumbnail)

        except Exception as ex:
               print('Exception has occured when scraping data! ' + str(ex))

        return content


