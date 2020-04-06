from bs4 import BeautifulSoup
import dateparser
import datetime
import requests
import codecs
from .config import DOMAIN_URL

class Scraper:
    """Scraper class"""
    def __init__(self, html):
        self.html = html
        self.soup = BeautifulSoup(html, "lxml")
        print(f"[Scraper] Retrieved page")

    def get_title(self):
        return self.soup.title.string

    def get_urls(self):
        """Scrapes posts on a page"""
        all_urls = []
        # infinite scroll
        urls = self.soup.find_all("a", class_="SQnoC3ObvgnGjWt90zD9Z _2INHSNB8V5eaWp4P0rY_mE")
        for url in urls:
            all_urls.append(url['href'])
        return all_urls

    def get_details(self):
        data = {}
        thread = self.soup.find_all('div', 'pagedlist_item')
        user_div = thread.pop()

        a = user_div.find('a', class_="user")
        data['text'] = self.soup.find('span', class_='rendered_qtext').get_text()
        data['user'] = {}
        try:
            data['user']['url'] = DOMAIN_URL+a['href']
            data['user']['name'] = a.get_text ()
        except:
            pass

        try:
            text = self.soup.find('p', class_="log_action_bar").get_text()
            split = text.split(' · ')
            date_time = split.pop().rstrip()
            data['datetime'] = str(dateparser.parse(date_time))
        except:
            data['datetime'] = str(datetime.datetime.now())

        return data

    def get_followers(self):
        links = self.soup.find_all("span", class_='list_count')
        try:
            span = links.pop()
            return span.text
        except:
            return []

    def get_topics(self):
        topics_ = self.soup.find_all('a', class_="topic_name")
        #TopicNameLink HoverMenu topic_name/HoverMenu TopicNameLink topic_name
        topics = []
        for topic in topics_:
            try:
                topics.append(str(topic.find('span', class_="TopicNameSpan").get_text()))
            except:
                pass
        return topics

    def get_answer_urls(self):
        all_answers_ = self.soup.find_all('a', class_='answer_permalink')
        answer_urls = []
        for ans in all_answers_:
            try:
                answer_urls.append(str(ans['href']))
            except:
                pass
        return answer_urls

    def get_full_answer(self, url):
        text_substr = r'{\\"text\\": \\"'
        text_substr_end = r'\\"'
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
        print(text)
        return text

    def get_related_questions(self):
        list_of_ques = self.soup.find_all('a', class_='question_link')
        related_questions = set()
        for elem in list_of_ques:
            try:
                address = str(elem['href'])
                if 'quora.com' not in address:
                    address = DOMAIN_URL+address
                related_questions.add(address)
            except:
                pass
        return list(related_questions)

    def get_user_stats(self):
        counts_ = self.soup.find_all('span', class_='list_count')
        counts = []
        for count in counts_:
            counts.append(count.get_text())
        return counts
