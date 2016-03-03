from spyders.spyder import Spyder
from bs4 import BeautifulSoup
from models.postmodel import PostModel
from models.content import Content

class QuickSpyder(Spyder):

    name = 'QuickSpyder'
    website = 'http://www.quickmeme.com/'

    def crawl(self, numberOfPages, minimumUpvotes, __blank):
        print(self.name + " " + self.spyder_reports.initializing())
        driver = self.get_configured_driver()

        print(self.spyder_reports.opening_website())
        driver.get(self.website)

        print(self.spyder_reports.scraping_data())
        scrapes = []
        for i in range(1, numberOfPages):
            driver.get(self.website + "page/" + str(i) + "/")
            posts = driver.find_elements_by_class_name("post")
            scrapes.extend(self.__scrape(posts, minimumUpvotes, __blank))
            print(self.spyder_reports.crawling_next())
        return scrapes



    def __scrape(self, posts, minimumUpvotes, __blank):
        results = []
        for ele in posts:
            html = ele.get_attribute('innerHTML')
            soup = BeautifulSoup(html, "html.parser")
            try:
                upvotes = soup.find("div",{'class':'sharecounts'})
                if upvotes is not None:
                    upvotes = upvotes.p
                if upvotes is not None:
                   likes = int(upvotes.text.replace(",","").replace(" shares", ""))
                   if likes > minimumUpvotes:
                      title = soup.find("h2", {'class':'post-title'})
                      content = Content()
                      content = self.__get_image_or_video(soup)
                      if content is not None and title is not None:
                        src = content.src
                        post = PostModel(title.text, src, content.type, src, likes)
                        results.append(post)
            except Exception as ex:
                   print('Exception has occured when scraping data! ' + str(ex))
        return results


    def __get_image_or_video(self, soup):
        content = Content()
        item = soup.find('img', {'class': 'post-image'})
        if item is not None:
            src = item.get('src')
            content.src = src
            if src.endswith(".gif"):
                content.type = "gif"
            else:
                content.type = "image"
            return content
        else:
            return None

