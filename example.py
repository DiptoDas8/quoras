from quoras import Quora

# login to Quora English platform
quora = Quora ('account-email-address', 'password', 'en')

# search for q/a threads containing 'ancient history' keywords
questions = quora.search('financi', 'question', scroll_count=3)
# same as above
questions = quora.search_posts('ancient history', scroll_count=3)

# search for users named "Dipto Das"
users = quora.search('Dipto Das', 'user', scroll_count=1)
# same as above
users = quora.search_users('Dipto Das', scroll_count=1)


# login to Quora Bengali platform
quora = Quora ('account-email-address', 'password', 'bn')

# search for details about a qathread
qathread_details = quora.search_url('https://bn.quora.com/আসামকে-কেন-সবাই-অসম-বলছে')

# search for details about a user
user_details = quora.search_url('https://www.quora.com/profile/Dipto-Das-1')

# search for the full text of an answer
full_answer = quora.get_full_answer('https://bn.quora.com/বিজ্ঞানীদের-মধ্যেও-কি/answers/150612153')