# quoras

A Python package to collect data from Quora.

## Installation
The package is available on PyPi. Simply run the following command:

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
This package allows you to call several functions. Search with keywords for questions or users with function `search(keyword, type='question', scroll_count=1)`. Change `type` to `'user'` to search user profiles. You can pass a value for `scroll_count` to control how many scrolls the web browser will automatically do.

```
questions = quora.search('ancient history', 'question', scroll_count=1)
users = quora.search('Dipto Das', 'user', scroll_count=1)
```

There are alternative ways to search posts or users. You can call `search_posts(keyword, scroll_count=1)` function that searches for posts with specified keyword without requiring explicitly indicating type. Similarly, `search_users(keyword, scroll_count=1)` function to search users containing keyword in their profile names. You can also pass a value for `scroll_count` to control how many scrolls the web browser will automatically do.

```
questions = quora.search_posts('ancient history', scroll_count=1)
users = quora.search_users('Dipto Das', scroll_count=1)
```

If you already have an url, you can directly search details about that entry. If it is an url to a Q/A thread, then it will return the question, topics, answers, participating users, and Quora suggested related questions. If it is an url to a user profile, then it will return statistics about the user (e.g., number of public answers, number of questions, number of shares, number of posts, number of followings, and number of followers), and links to top (defined by Quora) posts from the user. To use this function, you have to call `search_url(url)` function.

```
qathread_details = quora.search_url('https://bn.quora.com/দ্বিজাতি-তত্ত্ব-কী')
user_details = quora.search_url('https://www.quora.com/profile/Dipto-Das-1')
```