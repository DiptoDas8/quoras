import os
from .config import BASE_URL, DOMAIN_URL, QR_EMAIL, QR_PASSWORD
from .scraper import Scraper
from urllib.parse import unquote


class Quora:
    def __init__(self, browser):
        self.BASE_URL = BASE_URL
        self.DOMAIN_URL = DOMAIN_URL
        self.browser = browser

    def search_url(self, url, scroll_count=1):
        url = unquote (url)
        # Browser Actions
        b = self.browser
        b.get_home ()
        b.login (QR_EMAIL, QR_PASSWORD)
        b.get_url (url)
        b.infinite_scroll (scroll_count)

        u = Scraper (html=b.get_source ())
        datum = {}
        datum['url'] = url
        datum['question'] = str (u.get_title ()).split ('-')[0].strip ()
        datum['topics'] = u.get_topics ()
        datum['related_questions'] = u.get_related_questions ()
        datum['answers'] = []
        if url[-1] == '/':
            url = url[:-1]
        org_q = url.split ('/')[-1]
        # print(org_q)
        answer_urls = u.get_answer_urls ()
        # print ('length: ', len (answer_urls))
        for x in answer_urls:
            if org_q in x:
                if 'quora.com' in x:
                    pass
                else:
                    x = DOMAIN_URL + x
                answer = {}
                answer['url'] = x
                answer['full_answer'] = u.get_full_answer (x)
            datum['answers'].append (answer)

        return datum

    def search_posts(self, keyword, scroll_count):
        # Browser Actions
        b = self.browser
        b.get_home ()
        b.login (QR_EMAIL, QR_PASSWORD)
        b.search_by (keyword, 'question', scroll_count)
        b.infinite_scroll (scroll_count)
        our_urls = [unquote (link) for link in b.get_questions (scroll_count)]
        return our_urls

    def search_users(self, keyword, scroll_count):
        # Browser Actions
        b = self.browser
        b.get_home ()
        b.login (QR_EMAIL, QR_PASSWORD)
        b.search_by (keyword, 'user', scroll_count)
        b.infinite_scroll (scroll_count)
        user_urls = [unquote (link) for link in b.get_users (scroll_count)]
        return user_urls[1:]

    def search(self, keyword, type='question', scroll_count=1):
        if type == 'question':
            post_urls = self.search_posts (keyword, scroll_count)
            return post_urls
        elif type == 'user':
            user_urls = self.search_users (keyword, scroll_count)
            return user_urls

    def user_details(self, url, scroll_count):
        url = unquote(url)
        # Browser Actions
        b = self.browser
        b.get_home ()
        b.login (QR_EMAIL, QR_PASSWORD)

        b.get_url (url)
        u = Scraper (html=b.get_source ())

        user_details = {}
        user_details['user_display_name'] = str (u.get_title ()).split ('-')[0].strip ()
        print(user_details['user_display_name'])
        try:
            user_details['number_of_answers'], user_details['number_of_questions'], user_details['number_of_shares'],\
            user_details['number_of_posts'], user_details['number_of_followers'],\
            user_details['number_of_following'] = u.get_user_stats()
        except:
            pass
        b.infinite_scroll (scroll_count)
        user_details['answers'] = b.get_urls (url, 'answers', scroll_count)
        user_details['questions'] = b.get_urls(url, 'questions', scroll_count)
        user_details['shares'] = b.get_urls(url, 'shares', scroll_count)
        user_details['all_posts'] = b.get_urls(url, 'all_posts', scroll_count)
        user_details['followers'] = b.get_urls(url, 'followers', scroll_count)
        user_details['following'] = b.get_urls(url, 'following', scroll_count)

        return user_details
