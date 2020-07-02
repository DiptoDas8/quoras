from bs4 import BeautifulSoup
import dateparser
import datetime
import requests
import codecs
from urllib.parse import unquote
from langdetect import detect

class Scraper:
    """Scraper class"""
    def __init__(self, html):
        self.html = html
        self.soup = BeautifulSoup(html, "lxml")
        print(f"[Scraper] Retrieved page")

    def get_title(self):
        return self.soup.title.string

    def get_all_urls(self):
        content = str (self.soup)
        # print (content)
        text_substr = r'href="'
        text_substr_end = r'"'
        text_starts = [i for i in range (len (content)) if content.startswith (text_substr, i)]
        text_starts.append (len (content))
        substrings = []
        unicode_dirt = '\\'
        for i in range (1, len (text_starts) - 1):
            substring = content[text_starts[i] + len (text_substr):text_starts[i + 1]]
            end_idx = substring.find (text_substr_end)
            substring = substring[:end_idx].strip ().replace (unicode_dirt, '')
            substrings.append (substring)
        return substrings

    def get_topics(self):
        topics = []
        urls = self.get_all_urls()
        for url in urls:
            if 'topic' in url:
                pos = len('https://bn.quora.com/topic/')
                topic = url[pos:]
                topics.append(topic)
        return list(set(topics))

    def get_users(self):
        users = []
        urls = self.get_all_urls ()
        for url in urls:
            if 'profile' in url:
                pos = len ('https://bn.quora.com/profile/')
                profile = url[pos:]
                if profile!='Dipto-Das-1':
                    users.append (profile)
        return list(set(users))

    def get_answer_urls(self):
        answers = []
        urls = self.get_all_urls ()
        for url in urls:
            if 'answers' in url:
                answers.append(url)
        return answers

    def get_full_answer(self, url):
        # print('came here')
        text_substr = r'{\\\"text\\\": \\\"'
        text_substr_end = r'\\\"'
        content = requests.get (url).text
        # print(content)
        text_starts = [i for i in range (len (content)) if content.startswith (text_substr, i)]
        text_starts.append (len (content))
        substrings = []
        unicode_dirt = '\\'
        for i in range (1, len (text_starts) - 1):
            substring = content[text_starts[i] + len (text_substr):text_starts[i + 1]]
            end_idx = substring.find (text_substr_end)
            substring = substring[:end_idx].strip().replace(unicode_dirt,'').replace('u','\\u')
            try:
                substring = codecs.decode(substring, 'unicode_escape')
            except:
                pass
            substrings.append (substring)
        text = ' '.join (substrings).replace(unicode_dirt, '')
        return text

    def get_related_questions(self):
        answers = []
        urls = self.get_all_urls ()
        for url in urls:
            if 'https://bn.quora.com/' in url and \
                    not('answers' in url or 'topic' in url or 'profile' in url):
                answers.append (url)
        return answers

    def get_user_stats(self):
        content = str (self.soup)
        stats = [r'\"numPublicAnswers\":', r'\"numProfileQuestions\":', r'\"quoraSharesCount\":',
                 r'\"numTribePosts\":', r'\"followingCount\":', r'\"followerCount\":']
        counts = {}
        # print (content)
        for stat in stats:
            text_substr = stat
            text_substr_end = r','
            text_start = content.find(text_substr)+len(stat)
            text_end = content[text_start:].find(text_substr_end)
            # print(text_start)
            count = int(content[text_start:][:text_end])
            counts[stat.replace('\\','').replace(':','').replace('\"', '')] = count
        return counts
