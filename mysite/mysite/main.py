import requests
from bs4 import BeautifulSoup as bs

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import django
django.setup()

# newslist의 모델을 import 합니다
from newslist.models import NewsListData

def get_newslist(word): # 관련 검색어의 뉴스리스트들을 크롤링합니다.
    url = f'https://search.naver.com/search.naver?where=news&sm=tab_jum&query={word}'
    req = requests.get(url)
    html = req.text
    soup = bs(html, 'html.parser')

    datas = soup.findAll('a', attrs = {"class" : 'news_tit'})
    newslist = {}
    for data in datas:
        newslist[data.get('title')] = data.get('href')
    return newslist

def add_new_items(newslist, word): # DB에 크롤링한 정보들을 저장합니다.
    for title, link in newslist.items():
        NewsListData(keyword = word, title = title, link = link).save()
    print('done!')

# 이 명령어는 이 파일이 import가 아닌 python에서 직접 실행할 경우에만 아래 코드가 동작하도록 합니다.
if __name__ == '__main__':
    word = '황희찬'
    add_new_items(get_newslist(word), word)
