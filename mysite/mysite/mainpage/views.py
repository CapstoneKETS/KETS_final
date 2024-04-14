from django.shortcuts import render
import random
from .models import *


def index(request):
    # keyword_queryset = kwRank.objects.order_by('-rank')[:15]
    keyword_queryset = kwRank.objects.all()
    keyword_content = []
    for data in keyword_queryset:
        keyword_content.append({
            'rank': data.rank,
            'keyword': data.keyword,
            'datetime': data.datetime
        })
    print(keyword_content)

    old_queryset = kwHistory.objects.all()
    old_content = []
    for data in old_queryset:
        old_content.append({
            'rank': data.rank,
            'keyword': data.keyword,
            'datetime': data.datetime
        })
    print(old_content)

    # keyword_list.sort(key = lambda x: x[2])

    # random.shuffle(keyword_list)

    context = {
        'keyword_list': keyword_content,
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
    news_data = newsData.objects.filter(id=newsData_id)[0]
    news_data.summary = news_data.summary.split('<split>')
    content = {
        'news_data': news_data,
        'keyword': kwRank_keyword
    }
    return render(request, 'details/index.html', content)
