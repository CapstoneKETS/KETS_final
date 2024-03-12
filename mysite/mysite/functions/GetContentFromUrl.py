import time

import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import math
import numpy as np
from sklearn.preprocessing import normalize
from _datetime import datetime
import bs4
from time import *
import json
import schedule
from functions.Keyword import *
from functions.Preprocessing import *
from functions.SummarizeIn3Sentences import *
from mainpage.models import *

def dateForm(x):
    if (x > 0) & (x < 10):
        return '0' + str(x)
    else:
        return str(x)

def getSoup(url): # soup 객체를 가져옴
    res = requests.get(url)
    if res.status_code == 200:
        return bs(res.text, 'html.parser')
    else:
        print(f"Super big fail! with {res.status_code}")
        
def getNewslist(t): # 한 시간 동안(X시 대)의 뉴스 목록 가져오기 ex) 4시 48분일 경우 3:00~3:59의 기사를 가져옴
    time_now = gmtime(t + 28800) # 현재 시간보다 한 시간 전 GMT + 8
    time_bef = gmtime(t + 25200) # 현재 시간보다 두 시간 전 GMT + 7
    datetime_now = [time_now.tm_year, time_now.tm_mon, time_now.tm_mday, time_now.tm_hour]
    datetime_bef = [time_bef.tm_year, time_bef.tm_mon, time_bef.tm_mday, time_bef.tm_hour]

    #print(time_now)
    
    metadatas_tuple = readJson(datetime_now, datetime_bef)
    metadatas = []
    for metadata in metadatas_tuple:
        temp_dict = dict()
        temp_dict['oid'] = metadata[0]
        temp_dict['aid'] = metadata[1]
        temp_dict['datetime'] = metadata[2]
        metadatas.append(temp_dict)
    
    data_frame = pd.DataFrame(metadatas)
    print(data_frame)

    return metadatas

def getNewsdatas(metadatas):
    news_in_hour = []
    for metadata in metadatas:
        news_URL = 'https://sports.news.naver.com/news?oid=' + metadata['oid'] + '&aid=' + metadata['aid']
        news_in_hour.append(getNewsdata(news_URL))
    return news_in_hour

def getNewsdata(url): # 뉴스 본문 페이지에서 데이터들을 가져오는 함수
    soup = getSoup(url)
    title = soup.find('title').get_text()
    reporter = soup.select_one('#newsEndContents > div.reporter_area div.reporter_profile > div > div.profile_info > a > div.name').get_text()
    # reporter = soup.select_one('#newsEndContents > p.byline').get_text()
    company = soup.select_one('#content > div > div.content > div > div.link_news > div > h3 > span.logo').get_text()
    datetime = soup.select_one('#content > div > div.content > div > div.news_headline > div > span:nth-child(1)').get_text()
    datetime = getDatetimeFromNews(datetime)
    article = soup.find('div', attrs={"id": "newsEndContents"})
    for child in article.children:
        if isinstance(child, bs4.element.Tag):
            child.decompose()
    article = deleteChild(article).get_text()
    newsdata = {}
    newsdata['title'] = title
    newsdata['reporter'] = reporter
    newsdata['company'] = company
    newsdata['datetime'] = datetime
    newsdata['article'] = article
    newsdata['url'] = url
    return newsdata
    
def getDatetimeFromNews(datetime):
    datetime = re.split("[ .:]", datetime)
    if datetime[5] == "오후":
        datetime[6] = str(int(datetime[6]) + 12)
    datetime = datetime[1] + '.' + datetime[2] + '.' + datetime[3] + ' ' + datetime[6] + ':' + datetime[7]
    return datetime

def deleteChild(tag):
    for child in tag.children:
        if isinstance(child, bs4.element.Tag):
            child.decompose()
    return tag

def readJson(now, bef): # json 형식의 파일을 한 시간 단위로 긁어오기
    page = 1
    dup_cnt = 0
    metadatas = []
    while dup_cnt < 10:
        dup = 0
        news_list_URL = 'https://sports.news.naver.com/wfootball/news/list?isphoto=N&date=' + dateForm(now[0])\
                        + dateForm(now[1]) + dateForm(now[2]) + '&page=' + str(page)
        soup = str(getSoup(news_list_URL))
        news_metadata = json.loads(soup)
        for metadata in news_metadata['list']: # 뉴스 메타데이터 한 건 당
            for i in metadatas:
                if (i[0] == metadata['oid']) & (i[1] == metadata['aid']): # 메타데이터 중복 시
                    dup_cnt += 1
                    dup = 1
                    break
            if dup == 1: continue # 데이터가 중복일 경우 다음 메타데이터로 바로 넘어감
            datetime = re.split("[ .:]", metadata['datetime'])
            # 시간 단위들을 int형으로 변환
            for i in range(0, len(datetime)):
                datetime[i] = int(datetime[i])
            # 지금보다 한 시간 전일 경우 수집
            if (datetime[0] == now[0]) & (datetime[1] == now[1]) & (datetime[2] == now[2]) & (datetime[3] == now[3]): 
                metadata_tuple = (metadata['oid'], metadata['aid'], metadata['datetime'])
                metadatas.append(metadata_tuple)
                print(metadata_tuple)
            elif (datetime[0] == bef[0]) & (datetime[1] == bef[1]) & (datetime[2] == bef[2]) & (datetime[3] == bef[3]): # 두 시간 전 기사 만날 경우 끝
                return metadatas
        page += 1
    return metadatas

def insertNewsdata(data):
    t = newsData(title = data['title'],
                 reporter = data['reporter'],
                 company = data['company'],
                 datetime = data['datetime'],
                 summary = getSummary(data['article']),
                 url = data['url'])
    t.save()

def getKeywordsForKwhistory():
    news_list = getNewslist(time())
    news_datas = getNewsdatas(news_list)
    articles = []
    for data in news_datas:
        insertNewsdata(data)
        articles.append(data['article'])

    keyword = getKwFromArticles(articles)
    return keyword

def insertKwhistory():
    kws = getKeywordsForKwhistory()
    for kw in kws:
        t = kwHistory.objects.filter(keyword=kw[0], datetime=0)
        if len(t):
            t[0].rank += kw[1]
            t[0].save()
        else:
            t = kwHistory(keyword=kw[0], datetime=0, rank=kw[1])
            t.save()
    print(kws)

def deleteKwhistory(): # 24시간이 지난 키워드 삭제
    histories = kwHistory.objects.all().order_by('datetime')
    for history in histories:
        if history.datetime <= 23:
            history.datetime += 1
            history.save()
        else: history.delete()

def updateKwhistory():
    deleteKwhistory()
    insertKwhistory()

def updateKwrank():     # kwhistory -> kwrank
    kwRank.objects.all().delete()
    histories = kwHistory.objects.all()
    rank = dict()

    for history in histories:
        rank[history.keyword] = 0
    for history in histories:
        rank[history.keyword] += weightedrank(history.datetime) * history.rank

    keywords = list(rank)
    for keyword in keywords:
        t = kwRank(keyword=keyword, rank=rank[keyword])
        t.save()

def weightedrank(datetime):
    return 1 + (24-datetime) / 24

def updateKwtables():
    updateKwhistory()
    updateKwrank()
    showMeTables()

def showMeTables():
    kh = kwHistory.objects.all().order_by('-rank')
    kr = kwRank.objects.all().order_by('-rank')
    nd = newsData.objects.all()
    print(kh, kr, nd)
    for h in kh:
        print(h.keyword, h.datetime, h.rank)
    for r in kr:
        print(r.keyword, r.rank)
    for d in nd:
        print(d.title, d.reporter, d.company, d.summary)

def dropKwtables():
    kh = kwHistory.objects.all()
    for h in kh:
        h.delete()
    kr = kwRank.objects.all()
    for r in kr:
        r.delete()

if __name__ == '__main__':
    schedule.every().hour.at(":01").do(updateKwtables)
    # updateKwtables()

    while True:
        schedule.run_pending()
        print(gmtime(time()+32400))
        sleep(60)

    print(kwHistory.objects.all(), kwRank.objects.all(), "remain.")