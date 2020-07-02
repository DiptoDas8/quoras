# quoras

A Python package to collect data from Quora.

## Installation
The package is available on PyPI. Simply run the following command:

```
pip install quoras
```

## Setup
Create a folder called `chrome_path` in the same directory as your source file. Download the ChromeDriver from [here](https://sites.google.com/a/chromium.org/chromedriver/home) and place the `chromedriver.exe` file in the newly created folder.

## Initialize
You need to have account on Quora (or its language-specific forum) to collect data from it. Initialize the Quora class as following providing your credentials and language code. The language codes can be found [here](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes).

```
quora = Quora ('email-address', 'password', 'language-code')
```

## Usage
This package allows you to call several functions. Search with keywords for questions, topics or users with function `search(keyword, type='post', scroll_count=1)`. Change `type` to `'topic'` or `'user'` to search topic RSS pages or user profiles respectively. You can pass a value for `scroll_count` to control how many scrolls the web browser will automatically do.

```
posts = quora.search('ancient history', 'post', scroll_count=1)
topics = quora.search('finance', 'topic', scroll_count=1)
users = quora.search('Dipto Das', 'user', scroll_count=1)
```

There are alternative ways to search posts or users. You can call `search_posts(keyword, scroll_count=1)` function that searches for posts with specified keyword without requiring explicitly indicating type. Similarly, `search_users(keyword, scroll_count=1)` function to search users containing keyword in their profile names. You can also pass a value for `scroll_count` to control how many scrolls the web browser will automatically do.

```
questions = quora.search_posts('ancient history', scroll_count=1)
users = quora.search_users('Dipto Das', scroll_count=1)
```

To search for Q/A threads with a specific user-assigned topic tag, you can simply call `search_topic(topic, scroll_count=1)` function as follows:
```
topic_questions = search_topic('politics', scroll_count=5)
```

If you already have an url, you can directly search details about that entry. If it is an url to a Q/A thread, then it will return the question, topics, answers, participating users, and Quora suggested related questions. If it is an url to a user profile, then it will return statistics about the user (e.g., number of public answers, number of questions, number of shares, number of posts, number of followings, and number of followers), and links to top (defined by Quora) posts from the user. To use this function, you have to call `search_url(url)` function.

```
qathread_details = quora.search_url('https://bn.quora.com/আসামকে-কেন-সবাই-অসম-বলছে')
user_details = quora.search_url('https://www.quora.com/profile/Dipto-Das-1')
```

Importantly, quoras can can retrieve the full text in an answer given its url. For that, you need to call `get_full_answer(url)` function as following:

```
full_answer = quora.get_full_answer('https://bn.quora.com/বিজ্ঞানীদের-মধ্যেও-কি/answers/150612153')
```