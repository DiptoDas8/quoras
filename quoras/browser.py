import os
import time
import datetime
import dateparser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from urllib.parse import unquote


class Browser:
    """Browser class"""

    def __init__(self, language):
        # specifies the path to the chromedriver.exe
        GOOGLE_CHROME_PATH = './chrome_path' + '/chromedriver.exe'

        OPTION = Options()
        OPTION.add_argument("--disable-infobars")
        OPTION.add_argument("start-maximized")
        OPTION.add_argument("--disable-extensions")
        OPTION.add_argument("--headless")
        OPTION.add_argument("--disable-logging")
        OPTION.add_argument('log-level=3')
        # disable notifications popup alert
        OPTION.add_experimental_option(
            "prefs", {"profile.default_content_setting_values.notifications": 1}
        )
        self.driver = webdriver.Chrome(executable_path=GOOGLE_CHROME_PATH, chrome_options=OPTION)
        # self.driver = webdriver.PhantomJS()

        self.BASE_URL = 'https://www.quora.com'
        DOMAIN_URLS = {
            "en": 'https://quora.com',
            "bn": 'https://bn.quora.com',
            "hi": 'https://hi.quora.com',
            "es": 'https://es.quora.com',
            "fr": 'https://fr.quora.com',
            "jp": 'https://jp.quora.com'
        }
        self.DOMAIN_URL = DOMAIN_URLS[language]

        TITLE_PHRASES = {
            "bn": 'অনুসন্ধান করুন',
            "en": 'Search',
            "hi": 'ढूँढें',
            "es": 'Buscar',
            "fr": 'Rechercher',
            "jp": '検索',
        }

        self.TITLE_PHRASE = TITLE_PHRASES[language]

    def get_home(self):
        """Navigates to Nairaland mainpage"""
        url = self.BASE_URL
        self.driver.get(url)
        print("[Browser] Visiting Quora Homepage")

    def get_url(self, url):
        """Navigates to URL"""
        self.driver.get(url)
        print("[Browser] Visited ", url)

    def login(self, username, user_pass):
        form = self.driver.find_element_by_class_name('regular_login')
        email = form.find_element_by_name("email")
        email.send_keys(username)
        password = form.find_element_by_name("password")
        password.send_keys(user_pass)
        password.send_keys(Keys.RETURN)
        time.sleep(3)


    def search_by(self, search_keyword, type, scroll_count):
        """Initiate the search with keyword"""
        self.driver.get(self.DOMAIN_URL+'/search?q='+search_keyword+'&type='+type)
        self.infinite_scroll(scroll_count)
        # print(DOMAIN_URL+'/search?q='+search_keyword+'&type='+type)
        if self.TITLE_PHRASE in self.driver.title:
            print("Search succeeded")
        else:
            print('Something bad has happened: ', self.driver.title)
            exit()

    def search_rss(self, search_keyword, scroll_count):
        """Initiate the search with keyword"""
        self.driver.get (self.DOMAIN_URL + '/topic/' + search_keyword + '/all_questions/')
        self.infinite_scroll (scroll_count)
        if self.TITLE_PHRASE in self.driver.title:
            print ("Search succeeded")
        else:
            pass
            # print ('Something bad has happened: ', self.driver.title)
            # exit ()

    def infinite_scroll(self, limit=False):
        count = 0
        while count<limit:
            try:
                current = self.driver.page_source
                self.driver.execute_script ("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep (2)
                new = self.driver.page_source
                urls = len (self.driver.find_elements_by_class_name ("question_link"))
                if current == new:
                    return
                if limit and limit <= urls:
                    return
            except Exception as e:
                print(e)
            count += 1
            # print('*********%i*********'%count)

    def get_source(self):
        """Returns current page source html"""
        return self.driver.page_source.encode('utf-8')

    def get_questions(self, scroll_count):
        urls = []
        self.infinite_scroll(scroll_count)
        elems = self.driver.find_elements_by_class_name("question_link")
        for elem in elems:
            urls.append(unquote(elem.get_attribute("href")))
        return urls

    def get_users(self, scroll_count):
        urls = []
        self.infinite_scroll(scroll_count)
        elems = self.driver.find_elements_by_class_name("user")
        for elem in elems:
            elem = elem.get_attribute ("href")
            if elem is not None:
                urls.append (unquote(elem))
        return urls

    def get_topics(self, scroll_count):
        urls = []
        self.infinite_scroll (scroll_count)
        elems = self.driver.find_elements_by_class_name ("topic_name")
        for elem in elems:
            urls.append (unquote (elem.get_attribute ("href")))
        return urls

    def get_urls(self, url, category, scroll_count):
        url = unquote(url+'/'+category)
        self.driver.get (url)
        self.infinite_scroll(scroll_count)
        print ("[Browser] Visited to", url)
        if 'follow' in category:
            return self.get_users(scroll_count)
        else:
            return self.get_questions(scroll_count)
