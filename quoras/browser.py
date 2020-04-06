import os
import time
import datetime
import dateparser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from urllib.parse import unquote

from .config import BASE_URL, DOMAIN_URL, TITLE_PHRASE

class Browser:
    """Browser class"""

    def __init__(self, linux=False):
        # specifies the path to the chromedriver.exe
        GOOGLE_CHROME_PATH = './chrome_path/chromedriver.exe'

        if os.path.exists(GOOGLE_CHROME_PATH):
            print('Gooogle Chrome Path found')
        else:
            try:
                os.mkdir('./chrome_path')
            except:
                pass
            print('Download chromedriver for your OS from: https://chromedriver.storage.googleapis.com/index.html?path=80.0.3987.106/\n'
                  'Rename it to be chromedriver.exe\n'
                  'Place it in \'./chrome_path/\' directory with your python script.')
            exit(1)

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

    def get_home(self):
        """Navigates to Nairaland mainpage"""
        url = BASE_URL
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
        if 'Home - Quora' in self.driver.title:
            print('Quora Login successful')
        else:
            print('Quora Login failed: ', self.driver.title)
            exit()

    def search_by(self, search_keyword, type, scroll_count):
        """Initiate the search with keyword"""
        self.driver.get(DOMAIN_URL+'/search?q='+search_keyword+'&type='+type)
        self.infinite_scroll(scroll_count)
        # print(DOMAIN_URL+'/search?q='+search_keyword+'&type='+type)
        if TITLE_PHRASE in self.driver.title:
            print("Search succeeded")
        else:
            print('Something bad has happened: ', self.driver.title)
            exit()

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

    def get_urls(self, url, category, scroll_count):
        url = unquote(url+'/'+category)
        self.driver.get (url)
        self.infinite_scroll(scroll_count)
        print ("[Browser] Visited to", url)
        if 'follow' in category:
            return self.get_users(scroll_count)
        else:
            return self.get_questions(scroll_count)

    def get_comments(self, limit=None):
        all_comm = []

        comments = self.driver.find_elements_by_class_name('pagedlist_item')

        count = 0
        for comment in comments:
            if 'Sponsored' in comment.text:
                continue
            if limit and count >= limit:
                break
            count = count + 1
            data = {}
            data['user'] = {}
            try:
                div = comment.find_element_by_class_name('u-serif-font-main--large')
                div.find_element_by_class_name('ui_qtext_more_link').click()
            except:
                pass

            try:
                div = comment.find_element_by_class_name('u-serif-font-main--large')
                data['text'] = div.text
            except:
                continue

            try:
                user = comment.find_element_by_css_selector('a')

                if user:
                    data['user']['url'] = user.get_attribute('href')
                    data['user']['name'] = user.text
            except:
                pass

            try:
                text = comment.find('a', class_="_1sA-1jNHouHDpgCp1fCQ_F").get_text()
                data['user']['datetime'] = str(dateparser.parse(text))
            except:
                data['user']['datetime'] = str(datetime.datetime.now())
            all_comm.append(data)

        return all_comm
