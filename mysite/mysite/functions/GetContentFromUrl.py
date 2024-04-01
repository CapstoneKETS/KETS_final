import time
from time import *
import schedule
import math
from functions.Keyword import getKwFromArticles as keyBERT
from functions.Preprocessing import *
from functions.SummarizeIn3Sentences import getSummary as textRank
from functions.Crawling import *
from mainpage.models import *

def insertNewsdata(data):
    summary = textRank(data['article'])
    keyword = keyBERT(data['article'])
    keywords = ''
    for kw in keyword:
        keywords += (kw[0] + '*')
    t = newsData(title = data['title'],
                 reporter = data['reporter'],
                 company = data['company'],
                 datetime = data['datetime'],
                 summary = '<split>'.join(summary),
                 url = data['url'],
                 keywords = keywords)
    t.save()
    return keyword

def rankIdf(kw_list):
    print(kw_list)
    tf = {}
    n = len(kw_list)
    for kws in kw_list:
        for kw in kws:
            tf[kw[0]] = False
    for kws in kw_list:
        for kw in kws:
            if tf[kw[0]]:
                tf[kw[0]][0] += kw[1]
                tf[kw[0]][1] += 1
            else:
                tf[kw[0]] = [kw[1], 1]
    print(tf)
    for i in tf:
        tf[i] = tf[i][0] * math.log(n / (1 + tf[i][1]))
    return tf

def insertKwhistory(kw_list):
    histories = rankIdf(kw_list)
    for history in histories:
        t = kwHistory(keyword = history,
                      datetime = 0,
                      rank = histories[history])
        t.save()

def insertData():
    news_list = getNewslist(time())
    news_data = getNewsdata(news_list)
    kw_list = []
    for data in news_data:
        keyword = insertNewsdata(data)
        kw_list.append(keyword)
    return kw_list

def deleteKwhistory(): # 24시간이 지난 키워드 삭제
    histories = kwHistory.objects.all().order_by('datetime')
    for history in histories:
        if history.datetime <= 23:
            history.datetime += 1
            history.save()
        else: history.delete()

def updateKwhistory(kw_list):
    deleteKwhistory()
    insertKwhistory(kw_list)

def updateKwrank():     # kwhistory -> kwrank
    kwRank.objects.all().delete()
    histories = kwHistory.objects.all()
    rank = dict()

    for history in histories:
        rank[history.keyword] = 0
    for history in histories:
        rank[history.keyword] += weightedRank(history.datetime) * history.rank

    keywords = list(rank)
    for keyword in keywords:
        t = kwRank(keyword=keyword, rank=rank[keyword])
        t.save()

def weightedRank(datetime):
    return 1 + (24-datetime) / 24

def updateTables():
    kw_list = insertData()
    updateKwhistory(kw_list)
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
    nd = newsData.objects.all()
    for d in nd:
        d.delete()

if __name__ == '__main__':
    schedule.every().hour.at(":01").do(updateKwtables)
    # updateKwtables()

    while True:
        schedule.run_pending()
        print(gmtime(time()+32400))
        sleep(60)

    print(kwHistory.objects.all(), kwRank.objects.all(), "remain.")