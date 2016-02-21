import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from models.PostData import PostData
import time

class gagspyder(object):
    """9gag crawler"""
    def crawl(self, numberOfscrolls, minimumUpvotes):
        print('Initializing...')                             
        driver = self.__get_configured_driver()
        print('Opening website...')
        driver.get("http://9gag.com/")
        for i in range(0, numberOfscrolls):
             print('Scrolling down...')
             driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
             time.sleep(2) 

        print('Scraping data...')
       
        elements = driver.find_elements_by_class_name("badge-entry-container") #find articles (posts)
        scraped_data = self.__scrape_articles(elements, minimumUpvotes)
           
        print('Finished scraping...') 

        driver.quit()
        return scraped_data
    
    def __scrape_articles(self,articles,minimumUpvotes):
       
        results = []
        
        for ele in articles:          
            
            html = ele.get_attribute('innerHTML')
            soup = BeautifulSoup(html, "html.parser") 
            try:
                upvotes = soup.find("span",{'class':'badge-item-love-count'})            
                if upvotes is not None:
                   likes = int(upvotes.text.replace(",",""))
                   if likes > minimumUpvotes:
                      image = soup.find("img", {'class':'badge-item-img'}) #sometimes it's video so handle this case
                      title = soup.find("h2", {'class':'badge-item-title'})
                      if image is not None and title is not None: 
                        imageSrc = image.get('src')  
                        post = PostData(title.text, imageSrc, 'image', imageSrc, likes)                  
                        results.append(post)
            except Exception as ex:
                   print('Exception has occured when scraping data! ' + ex)      
        return results
       
    def __get_configured_driver(self):
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36")
        driver = webdriver.PhantomJS(desired_capabilities=dcap)
        driver.set_window_size(1120, 550)
       
        return driver


























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

