from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class SpyderWeb(object):

        @staticmethod
        def get_scroll_down_js():
            return "window.scrollTo(0, document.body.scrollHeight);"

        @staticmethod
        def get_scroll_down_js(pixels):
            return "window.scrollTo(0, " + str(pixels) + ");"

        @staticmethod
        def get_click_elements_by_class(class_name):
            return "jQuery('." + class_name + "').click();"

class SpyderReports(object):

    @staticmethod
    def initializing():
        return "Initializing..."

    @staticmethod
    def opening_website():
        return "Opening website..."

    @staticmethod
    def logging_in():
        return "'Loggin in...'"

    @staticmethod
    def scrolling_down():
        return "Scrolling down..."

    @staticmethod
    def scrapable_objects_found(number):
        return "Number of scrapable objects found: " + str(number) + "!"

    @staticmethod
    def scraping_data():
        return "Scraping data..."
    @staticmethod
    def crawling_next():
        return "Crawling next page..."
    @staticmethod
    def end_reach():
        return "End of web..."

    @staticmethod
    def finished_scraping():
        return "'Finished scraping...'"

class Spyder(object):

    name = ''
    website = ''
    username = ''
    password = ''
    spyder_web = SpyderWeb
    spyder_reports = SpyderReports
    default_thumbnail = 'http://4dlols.com/wp-content/uploads/2016/03/logo_beta2_partial_text.png'

    def crawl(self):
        pass

    def __scrape(self):
        pass

    def gather_web(self, page_source):
        f = open("pagesource_" + self.name, "w")
        f.write(str(page_source.encode("utf8")))
        f.close()

    @staticmethod
    def get_configured_driver():
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36")
        driver = webdriver.PhantomJS(desired_capabilities=dcap)
        driver.set_window_size(1120, 550)

        return driver





