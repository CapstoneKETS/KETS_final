from django.shortcuts import render
import random
from .models import *


def index(request):
    keyword_queryset = kwRank.objects.order_by('-rank')[:15]
    keyword_content = []
    hour = []
    for i, data in zip(range(1,16), keyword_queryset):
        keyword_content.append({
            'rank': i,
            'keyword': data.keyword,
            'datetime': data.datetime
        })
        hour.append(data.datetime)

    random.shuffle(keyword_content)
    hour = set(hour)

    print(keyword_content)
    print(hour)

    context = {
        'keyword_list': keyword_content,
        'hour': hour,
    }
    return render(request, 'mainpage/index.html', context)

def newsList(request, kwRank_keyword):
    newslist_data = newsData.objects.filter(keywords__contains=kwRank_keyword)[:5]
    newslist_content = []
    for data in newslist_data:
        if data:  # newslistData가 None이 아닌 경우에만 추가
            newslist_content.append({
                'id': data.id,
                'title': data.title,
                'company': data.company,
                'reporter': data.reporter,
                'datetime': data.datetime
            })
    print(newslist_content)
    content = {
        'newslist_content': newslist_content,
        'keyword' : kwRank_keyword
    }
    return render(request, 'newslist/index.html', content)

def details(request, kwRank_keyword, newsData_id):
    newslist_data = newsData.objects.filter(keywords__contains=kwRank_keyword)[:5]
    newslist_content = []
    for data in newslist_data:
        if data and data.id != newsData_id:  # 선택된 newsData의 id와 같지 않은 것만 추가
            newslist_content.append({
                'id': data.id,
                'title': data.title,
                'company': data.company,
            })

    news_data = newsData.objects.filter(id=newsData_id)[0]
    news_data.summary = news_data.summary.split('<split>')
    content = {
        'newslist': newslist_content,
        'news_data': news_data,
        'keyword': kwRank_keyword
    }
    return render(request, 'details/index.html', content)
