from pprint import pprint
from quoras import Browser, Quora
import json

def main():
    browser = Browser(linux=False)
    quora = Quora(browser)

    # # keywords ---- DONE
    engk = 'ancient history'
    benk = 'ইতিহাস'
    hink = 'भारत पाकिस्तान'
    espk = 'historia antigua'
    frek = 'histoire ancienne'
    japk = '古代史'
    engu = 'jules'
    # # search keyword --- DONE
    result = quora.search(engk, type='question', scroll_count=1)
    pprint(result)

    # # questions --- DONE
    engq = 'https://www.quora.com/What-are-the-weirdest-facts-about-India/'
    engq = 'https://www.quora.com/Why-do-people-still-believe-in-evolution-If-you-know-ancient-history-you-would-know-its-all-made-up-nonsense'
    benq = 'https://bn.quora.com/%E0%A6%A6%E0%A7%8D%E0%A6%AC%E0%A6%BF%E0%A6%9C%E0%A6%BE%E0%A6%A4%E0%A6%BF-%E0%A6%A4%E0%A6%A4%E0%A7%8D%E0%A6%A4%E0%A7%8D%E0%A6%AC-%E0%A6%95%E0%A7%80'
    hinq = 'https://hi.quora.com/%E0%A4%A8%E0%A4%B0%E0%A5%87%E0%A4%82%E0%A4%A6%E0%A5%8D%E0%A4%B0-%E0%A4%AE%E0%A5%8B%E0%A4%A6%E0%A5%80-%E0%A4%95%E0%A5%87-%E0%A4%AC%E0%A4%BE%E0%A4%B0%E0%A5%87-%E0%A4%AE%E0%A5%87%E0%A4%82-%E0%A4%95%E0%A5%81%E0%A4%9B'
    espq = 'https://es.quora.com/Es-muy-dif%C3%ADcil-aprender-a-programar-Python'
    freq = 'https://fr.quora.com/Quel-est-un-inconv%C3%A9nient-de-Python'
    japq = 'https://jp.quora.com/Python%E3%81%A7%E3%81%AF%E4%BD%95%E3%82%92%E6%A7%8B%E7%AF%89%E3%81%97%E3%81%9F%E3%82%8A%E7%A8%BC%E5%83%8D%E3%81%95%E3%81%9B%E3%81%9F%E3%82%8A%E3%81%A7%E3%81%8D%E3%81%BE%E3%81%99%E3%81%8B-%E3%83%97%E3%83%AD%E3%82%B0'

    # # search question url --- DONE
    result = quora.search_url(engq, scroll_count=10000000)
    pprint(result)

    # # user search - DONE
    benu = 'https://bn.quora.com/profile/%E0%A6%86%E0%A6%A6%E0%A6%BF%E0%A6%A4%E0%A7%8D%E0%A6%AF-%E0%A6%95%E0%A6%AC%E0%A6%BF%E0%A6%B0-Aditya-Kabir'
    engu = 'https://en.quora.com/profile/Thomas-Cormen-1'
    result = quora.user_details(benu, scroll_count=1)
    pprint(result)

    with open ('filename.json', 'w', encoding='utf8') as json_file:
        json.dump (result, json_file, ensure_ascii=False, indent=4)


main()
