import requests
from bs4 import BeautifulSoup as bs
import bs4
import re
from time import *
import json

def dateForm(x):
    if (x > 0) & (x < 10):
        return '0' + str(x)
    else:
        return str(x)

def getSoup(url):  # soup 객체를 가져옴
    res = requests.get(url)
    if res.status_code == 200:
        return bs(res.text, 'html.parser')
    else:
        print(f"Super big fail! with {res.status_code}")

def getJson(url):
    # URL에 GET 요청을 보내고 응답을 받음
    response = requests.get(url)

    # 요청이 성공했을 때
    if response.status_code == 200:
        # JSON 형식의 데이터를 파이썬 데이터로 로드하여 반환
        return response.json()
    else:
        print('Failed to retrieve data. Status code:', response.statuscode)
        return None

def getNewslist(t):  # 한 시간 동안(X시 대)의 뉴스 목록 가져오기 ex) 4시 48분일 경우 3:00~3:59의 기사를 가져옴
    time_now = gmtime(t + 28800)  # 현재 시간보다 한 시간 전 GMT + 8
    time_bef = gmtime(t + 25200)  # 현재 시간보다 두 시간 전 GMT + 7
    datetime_now = [time_now.tm_year, time_now.tm_mon, time_now.tm_mday, time_now.tm_hour]
    datetime_bef = [time_bef.tm_year, time_bef.tm_mon, time_bef.tm_mday, time_bef.tm_hour]

    metadatas_tuple = readJson(datetime_now, datetime_bef)
    metadatas = []
    for metadata in metadatas_tuple:
        temp_dict = dict()
        temp_dict['oid'] = metadata[0]
        temp_dict['aid'] = metadata[1]
        temp_dict['datetime'] = metadata[2]
        metadatas.append(temp_dict)

    return metadatas


def getNewsdata(metadatas):
    news_in_hour = []
    for metadata in metadatas:
        news_URL = 'https://sports.news.naver.com/news?oid=' + metadata['oid'] + '&aid=' + metadata['aid']
        news_in_hour.append(getNewsdatum(news_URL))
    return news_in_hour


def getNewsdatum(url):  # 뉴스 본문 페이지에서 데이터들을 가져오는 함수
    soup = getSoup(url)
    print(url)
    newsdata = {}
    newsdata['title'] = soup.find('title')
    newsdata['reporter'] = soup.select_one(
        '#newsEndContents > div.reporter_area div.reporter_profile > div > div.profile_info > a > div.name')
    # reporter = soup.select_one('#newsEndContents > p.byline').get_text()
    newsdata['company'] = soup.select_one('#content > div > div.content > div > div.link_news > div > h3 > span.logo')
    newsdata['datetime'] = soup.select_one(
        '#content > div > div.content > div > div.news_headline > div > span:nth-child(1)')
    newsdata['article'] = soup.find('div', attrs={"id": "newsEndContents"}).deleteChild(newsdata['article'])

    for t in newsdata:
        if t is None:
            t = ' '
        else: t = t.get_text()

    newsdata['datetime'] = getDatetimeFromNews(newsdata['datetime'])
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


def readJson(now, bef):  # json 형식의 파일을 한 시간 단위로 긁어오기
    page = 1
    dup_cnt = 0
    metadatas = []
    while dup_cnt < 10:
        dup = 0
        news_list_URL = 'https://sports.news.naver.com/wfootball/news/list?isphoto=N&date=' + dateForm(now[0]) \
                        + dateForm(now[1]) + dateForm(now[2]) + '&page=' + str(page)
        print(news_list_URL)
        news_metadata = getJson(news_list_URL)
        for metadata in news_metadata['list']:  # 뉴스 메타데이터 한 건 당
            for i in metadatas:
                if (i[0] == metadata['oid']) & (i[1] == metadata['aid']):  # 메타데이터 중복 시
                    dup_cnt += 1
                    dup = 1
                    break
            if dup == 1: continue  # 데이터가 중복일 경우 다음 메타데이터로 바로 넘어감
            datetime = re.split("[ .:]", metadata['datetime'])
            # 시간 단위들을 int형으로 변환
            for i in range(0, len(datetime)):
                datetime[i] = int(datetime[i])
            # 지금보다 한 시간 전일 경우 수집
            if (datetime[0] == now[0]) & (datetime[1] == now[1]) & (datetime[2] == now[2]) & (datetime[3] == now[3]):
                metadata_tuple = (metadata['oid'], metadata['aid'], metadata['datetime'])
                metadatas.append(metadata_tuple)
                print(metadata_tuple)
            elif (datetime[0] == bef[0]) & (datetime[1] == bef[1]) & (datetime[2] == bef[2]) & (
                    datetime[3] == bef[3]):  # 두 시간 전 기사 만날 경우 끝
                return metadatas
        page += 1
    return metadatas