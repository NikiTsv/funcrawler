#http://www.gifbin.com/
from spyders.spyder import Spyder
from bs4 import BeautifulSoup
from models.postmodel import PostModel
from models.content import Content
from selenium.webdriver.common.keys import Keys
import time

class BinSpyder(Spyder):

    name = 'BinSpyder'
    website = "http://gifbin.com"

    def crawl(self, numberOfPages, minimumUpvotes, __blank):
        print(self.name + " " + self.spyder_reports.initializing())
        driver = self.get_configured_driver()

        print(self.spyder_reports.opening_website())
        driver.get(self.website)
        print(self.spyder_reports.scraping_data())
        scrapes = []
        for i in range(0, numberOfPages):
            post = driver.find_element_by_id("main")
            scrapes.extend(self.__scrape(post, minimumUpvotes))
            nextLink = driver.find_elements_by_xpath("//ul[@id='gif-nav']/li/a")
            nextLink[1].send_keys(Keys.ENTER)
            print(self.spyder_reports.crawling_next())
            #driver.save_screenshot('reddit-nextpage_' + str(i) + '.png')
            time.sleep(1.5)

        driver.quit()
        return scrapes

    def __scrape(self, posts, minimumUpvotes):

        results = []
        ele = posts
        html = ele.get_attribute('innerHTML')
        soup = BeautifulSoup(html, "html.parser")
        try:
            upvotes = soup.find("div", {'class': 'ratingblock'})
            if upvotes is not None:
               parseRating = upvotes.text.split("Rating: ")[1].split("(")[0].split("/")[0] #ugly but easy.

               likes = float(parseRating)

               if likes > minimumUpvotes:
                  title = soup.find("h1")
                  content = Content()
                  content = self.__get_image_or_video(soup)
                  likes = int(likes * 1000) #it's rating 3.5/5
                  if content is not None and title is not None:
                    src = content.src
                    post = PostModel(title.text, src, content.type, src, likes, content.thumbnail)
                    results.append(post)
        except Exception as ex:
               print('Exception has occured when scraping data! ' + str(ex))
        return results

    def __get_image_or_video(self, soup): #more like get video
        content = Content()
        video = soup.find('video')
        if video is not None:
            src = soup.findAll('source')[1]
            src = src.get("src")
            content.src = src
            content.type = 'video/mp4'
            thumbnail =  video.get("poster")
            content.thumbnail = self.website + thumbnail
            return content
        else:
            return None


