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
    def crawl(self):
        print(self.name + " " + self.spyder_reports.initializing())
        driver = self.get_configured_driver()
        print(self.spyder_reports.opening_website())
        driver.get(self.website)
        print(self.spyder_reports.scraping_data())
        post = driver.find_element_by_tag_name('body')
        scrapes = self.__scrape(post)
        driver.quit()
        return scrapes

    def __scrape(self, post):
        html = post.get_attribute('innerHTML')
        soup = BeautifulSoup(html, "html.parser")
        try:
           video = soup.find('video')
           thumbnail = video.get('poster')
           source = soup.find('source')
           src = source.get('src')
           content = Content('video/mp4', src, thumbnail)

        except Exception as ex:
               print('Exception has occured when scraping data! ' + str(ex))

        return content


