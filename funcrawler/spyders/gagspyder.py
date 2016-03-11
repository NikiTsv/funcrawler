from spyders.spyder import Spyder
from bs4 import BeautifulSoup
from models.postmodel import PostModel
from models.content import Content
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

class GagSpyder(Spyder):

    name = 'GagSpyder'
    website = "http://9gag.com"
    username = 'n1gh7b1rd'
    password = 'kodkod'

    def crawl(self, numberOfscrolls, minimumUpvotes, minimumComments):
        print(self.name + " " + self.spyder_reports.initializing())
        driver = self.get_configured_driver()

        print(self.spyder_reports.opening_website())
        driver.get(self.website)
        print(self.spyder_reports.logging_in())
        self.__login(driver, self.username, self.password)

        for i in range(0, numberOfscrolls):
             print(self.spyder_reports.scrolling_down() + str(i))
             driver.execute_script(self.spyder_web.get_scroll_down_js(500))
             time.sleep(0.4)
             if i % 50 == 0:
                 #trying to prevend idle
                 #ActionChains(driver).move_by_offset(2, 2)
                 #ActionChains(driver).send_keys(Keys.ESCAPE)
                 try:
                    driver.find_element_by_class_name("badge-btn-close").send_keys(Keys.ENTER)
                 except: pass
             if i % 500 == 0:
                 driver.save_screenshot("after_scrolls_" + str(i) + ".png")
             #TODO: HANDLE LOAD MORE BUTTON?

        driver.save_screenshot("after_scrolls" + ".png")
        posts = driver.find_elements_by_class_name("badge-entry-container")
        print(self.spyder_reports.scrapable_objects_found(len(posts)))
        print(self.spyder_reports.scraping_data())
        page_source = driver.page_source
        scraped_data = self.__scrape(page_source, minimumUpvotes, minimumComments)
           
        print(self.spyder_reports.finished_scraping())

        driver.quit()
        return scraped_data
    
    def __scrape(self, page_source, minimumUpvotes, minimumComments):

        results = []
        soup = BeautifulSoup(page_source, "html.parser")
        #save source
        self.gather_web(soup.prettify())
        articles = soup.findAll("article", "badge-entry-container")
        for ele in articles:
            try:
                upvotes = ele.find("span", {'class': 'badge-item-love-count'})
                comments = ele.find("a", {'class': 'comment'})
                if upvotes is not None:
                   likes = int(upvotes.text.replace(",", ""))
                   if likes > minimumUpvotes or \
                           (comments is not None and int(comments.text.replace(" comments", "")) > minimumComments):
                      title = ele.find("h2", {'class': 'badge-item-title'})
                      content = Content()
                      content = self.__get_image_or_video(ele)
                      if content is not None and title is not None:
                        src = content.src
                        post = PostModel(title.text, src, content.type, src, likes, content.thumbnail)
                        results.append(post)
            except Exception as ex:
                   print('Exception has occured when scraping data! ' + str(ex))
        return results

    def __get_image_or_video(self, ele):
        content = Content()
        video = ele.find("source")
        if video is not None:
            content.type = 'video/mp4'
            content.src = video.get('src')
            thumbnail = ele.find("img", {'class': 'badge-item-img'})
            if thumbnail is not None:
                thumbnail = thumbnail.get('src')
                content.thumbnail = thumbnail
            else:
                content.thumbnail = ''
            return content
        else:
             image = ele.find("img", {'class': 'badge-item-img'})
             if image is not None:
                content.type = 'image'
                content.src = image.get('src')
                content.thumbnail = ''
                return content
             else: return None

    def __login(self, driver, username, password):
        driver.find_elements_by_class_name("badge-login-button")[0].click()
        driver.save_screenshot('login-click1.png')
        time.sleep(2)
        driver.find_element_by_id("jsid-login-email-name").send_keys(username)
        driver.find_element_by_id("login-email-password").send_keys(password)
        qq = driver.find_element_by_xpath("//form[@id='login-email']/div[3]/input")
        qq.click()
        time.sleep(2)
        driver.save_screenshot('login-click2.png')




    #<a class="btn badge-load-more-post blue" href="/?id=a8MqP6p%2Cayd239y%2CaA102Vg&amp;c=300" data-loading-text="Loading more posts..." data-load-count-max="30">I want more fun</a>






        '''example shit'''
        #driver.find_element_by_id('search_form_input_homepage').send_keys("realpython")
        #driver.find_element_by_id("search_button_homepage").click()

        '''example shit'''
        #url = "http://9gag.com/"
        #source_code = requests.get(url)
        #plain_text = source_code.text
        #soup = BeautifulSoup(plain_text)
        #articles = soup.findAll('article',{'class':'badge-entry-container'})
        #for  article in articles:
        #    img = article.findChildren('img',{'class': 'badge-item-img'})
        #    imgLink = img[0].get('src')
        #    print(imgLink)


        #for article in soup.findAll('article', {'class': 'badge-entry-container'}):
        #    mainDiv =  article.find('div', {'class': 'badge-post-container'})
        #    image = mainDiv.findAll()
        #    picUrl = image.get('href')
        #    print(picUrl)