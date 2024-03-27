from django.shortcuts import render
import random
from .models import *


def index(request):
    # context = dict()

    # for i in range(1, 16):
    #     context[i] = keyword
    #
    # print(context)
    keyword_queryset = kwRank.objects.order_by('-rank')[:15]
    keyword_list = list(keyword_queryset)
    keyword_dict = {}
    # for i in keyword_list:

    # random.shuffle(keyword_list)

    context = {
        'keyword_list': keyword_list,
    }
    return render(request, 'mainpage/index.html', context)

def newsList(request):

    newslist_data = newsData.objects.all()[:5]
    newslist_content = []
    for data in newslist_data:
        if data:  # newslistData가 None이 아닌 경우에만 추가
            newslist_content.append({
                'title': data.title,
                'company': data.company,
                'reporter': data.reporter,
                'datetime': data.datetime # 각각의 요소에서 newslistData를 지웠습니다. 혹시
            })
    print(newslist_content)
    content = {
        'newslist_content': newslist_content
    }
    return render(request, 'newslist/index.html', content)

def details(request):
    # details = newsData.objects
    #미완성. newsData에서 요약문을 가져올 방법을 찾는 중입니다.
    return render(request, 'details/index.html')
