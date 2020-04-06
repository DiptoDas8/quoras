import json

with open ('./settings.json') as json_file:
    config = json.load (json_file)

BASE_URL = 'https://www.quora.com'

QR_EMAIL = config['email']
QR_PASSWORD = config['password']


language = config['language']
DOMAIN_URLS = {
    "en": 'https://quora.com',
    "bn": 'https://bn.quora.com',
    "hi": 'https://hi.quora.com',
    "es": 'https://es.quora.com',
    "fr": 'https://fr.quora.com',
    "jp": 'https://jp.quora.com'
}
DOMAIN_URL = DOMAIN_URLS[language]

TITLE_PHRASES = {
    "bn": 'অনুসন্ধান করুন',
    "en": 'Search',
    "hi": 'ढूँढें',
    "es": 'Buscar',
    "fr": 'Rechercher',
    "jp": '検索',
}

TITLE_PHRASE = TITLE_PHRASES[language]
