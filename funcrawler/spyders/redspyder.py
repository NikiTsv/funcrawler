#https://www.reddit.com/domain/i.imgur.com/controversial
from spyders.spyder import Spyder
from spyders.smallspyder import SmallSpyder
from bs4 import BeautifulSoup
from models.postmodel import PostModel
from models.content import Content
from selenium.webdriver.common.keys import Keys
import time

class RedSpyder(Spyder):

    name = 'RedSpyder'
    website = "https://www.reddit.com/domain/i.imgur.com/controversial"

    websites = ["https://www.reddit.com/r/funny"]
                # ,"https://www.reddit.com/domain/i.imgur.com/controversial",
                # "https://www.reddit.com/domain/gfycat.com/"]

    def __crawl(self, numberOfPages, minimumUpvotes, website):
        print(self.name + " " + self.spyder_reports.initializing())
        driver = self.get_configured_driver()

        print(self.spyder_reports.opening_website())
        driver.get(website)
        print(self.spyder_reports.scraping_data())
        scrapes = []
        for i in range(0, numberOfPages):
            self.__expand_videos(driver)
            posts = driver.find_elements_by_css_selector('.thing')
            scrapes.extend(self.__scrape(posts, minimumUpvotes))
            nextLink = driver.find_elements_by_xpath("//span[contains(@class, 'nextprev')]/a")
            #driver.save_screenshot('reddit-nextpage_' + str(i) + '.png')
            try:
                if len(nextLink) == 1:
                   nextLink[0].send_keys(Keys.ENTER)
                else:
                   nextLink[1].send_keys(Keys.ENTER)
                time.sleep(2.5)
                print(self.spyder_reports.crawling_next())
            except IndexError:
                print(self.spyder_reports.end_reach())
                break

        driver.quit()
        return scrapes

    #<div class="expando-button video expanded"></div> #expands video posts
    def __expand_videos(self, driver):
        driver.execute_script(self.spyder_web.get_click_elements_by_class('expando-button'))
        time.sleep(2)
        #driver.save_screenshot('reddit-expanded-videos.png')

    def crawl(self, numberOfPages, minimumUpvotes, __blank):
        scrapes = []
        for website in self.websites:
            scrapes.extend(self.__crawl(numberOfPages, minimumUpvotes, website))
        return scrapes

    def __scrape(self, posts, minimumUpvotes):
        results = []
        for ele in posts:
            html = ele.get_attribute('innerHTML')
            soup = BeautifulSoup(html, "html.parser")
            #self.gather_web(soup.prettify())
            try:
                upvotes = soup.find("div",{'class': 'score unvoted'})
                if upvotes is not None:
                   if upvotes.text == '•':
                      continue
                   likes = int(upvotes.text)

                   if likes > minimumUpvotes:
                      title = soup.find("a", {'class': 'title'})
                      content = Content()
                      content = self.__get_image_or_video(soup)
                      if content is not None and title is not None:
                        src = content.src
                        post = PostModel(title.text, src, content.type, src, likes, content.thumbnail)
                        results.append(post)
            except Exception as ex:
                   print('Exception has occured when scraping data! ' + str(ex))
        return results

    #video: <a class="title may-blank " href="http://i.imgur.com/C4MLOlJ.gifv" tabindex="1">That's why you should check your webcam first</a>
    #normal: <a class="title may-blank " href="http://i.imgur.com/YE0RTZP.jpg" tabindex="1">What could go wrong?</a>
    #normal: <a class="title may-blank " href="http://i.imgur.com/YE0RTZP.png" tabindex="1">What could go wrong?</a>
    def __get_image_or_video(self, soup):

        #TODO: implement small spyder funcionality
        content = Content()
        link = soup.find("a", {'class': 'title'})
        if link is not None:
            video = soup.find("div", {'class': 'expando-button'})  # this means it's a gif or video
            if video is not None:
                agent = SmallSpyder(link.get('href'))
                content = agent.crawl_content()
            else:
                content.src = link.get('href')
                content.type = 'image'
                content.thumbnail = ''

        return content



        # content = Content()
        # link = soup.find("a", {'class': 'title'})
        # if link is not None:
        #     video = soup.find("video", {'class': 'vjs-tech'})
        #     if video is not None:
        #         content.src = video.get('src')
        #         content.type = 'video/mp4'
        #         thumbnail = soup.find("a", {'class': 'thumbnail'})
        #         if thumbnail is not None:
        #             thumbnail = thumbnail.get('href')
        #             content.thumbnail = thumbnail
        #         else:
        #             content.thumbnail = self.default_thumbnail
        #     else:
        #         content.src = link.get('href')
        #         content.type = 'image'
        #         content.thumbnail = ''

            # if src.endswith(".gifv"):
            #     content.type = 'video/mp4'
            #     thumbnail = soup.find("a", {'class': 'thumbnail'})
            #     if thumbnail is not None:
            #         thumbnail = thumbnail.get('href')
            #         content.thumbnail = thumbnail
            #     else:
            #         #default, TODO: get it out of here
            #         content.thumbnail = self.default_thumbnail
            # else:
            #     content.type = 'image'
            #     content.thumbnail = ''
            #return content
        # else:
        #     return None


