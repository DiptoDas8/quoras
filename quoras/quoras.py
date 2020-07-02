import os
from .scraper import Scraper
from urllib.parse import unquote
from .browser import Browser


class Quoras:
    def __init__(self, email, password, language='en'):
        self.browser = Browser(language)
        self.BASE_URL = self.browser.BASE_URL
        self.DOMAIN_URL = self.browser.DOMAIN_URL
        self.browser.get_home()
        self.browser.login(email, password)

    def search_url(self, url):
        url = unquote (url)
        # Browser Actions
        b = self.browser
        b.get_url (url)

        u = Scraper (html=b.get_source ())
        datum = {}
        if 'profile' not in url:
            datum['url'] = url
            datum['question'] = u.get_title ()
            datum['topics'] = u.get_topics ()
            datum['related_questions'] = u.get_related_questions ()
            datum['answers'] = u.get_answer_urls ()
            datum['users'] = u.get_users()
            if url[-1] == '/':
                url = url[:-1]
            # org_q = url.split ('/')[-1]
            # print(org_q)
            # u.get_full_answer('') ___ WORKS
            # print ('length: ', len (answer_urls))
        else:
            datum['url'] = url
            datum['stats'] = u.get_user_stats()
            datum['answers'] = u.get_answer_urls ()

        return datum

    def get_full_answer(self, url):
        url = unquote (url)
        # Browser Actions
        b = self.browser
        b.get_url (url)

        u = Scraper (html=b.get_source ())
        full_answer = u.get_full_answer(url)
        return full_answer

    def search_posts(self, keyword, scroll_count=1):
        # Browser Actions
        b = self.browser
        b.search_by (keyword, 'question', scroll_count)
        post_urls = [unquote (link) for link in b.get_questions (scroll_count)]
        return post_urls

    def search_users(self, keyword, scroll_count=1):
        # Browser Actions
        b = self.browser
        b.search_by (keyword, 'user', scroll_count)
        user_urls = [unquote (link) for link in b.get_users (scroll_count)]
        return user_urls[1:]

    def search_rss(self, keyword, scroll_count=1):
        # Browser Actions
        b = self.browser
        b.search_by (keyword, 'topic', scroll_count)
        rss_urls = [unquote (link) for link in b.get_topics(scroll_count)]
        return rss_urls

    def search(self, keyword, type='post', scroll_count=1):
        if type == 'post':
            post_urls = self.search_posts (keyword, scroll_count)
            return post_urls
        elif type == 'user':
            user_urls = self.search_users (keyword, scroll_count)
            return user_urls
        elif type == 'topic':
            rss_urls = self.search_rss (keyword, scroll_count)
            return rss_urls

    def search_topic(self, topic, scroll_count=1):
        # Browser Actions
        b = self.browser
        b.search_rss(topic, scroll_count)
        post_urls = [unquote (link) for link in b.get_questions (scroll_count)]
        return post_urls
