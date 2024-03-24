from django.shortcuts import render
import requests
from .models import newsList

def index(request):

    newslist_data = NewsListData.objects.all()[:5]
    newslist_content = []
    for data in newslist_data:
        if data.newslistData:  # newslistData가 None이 아닌 경우에만 추가
            newslist_content.append({
                'title': data.newslistData.title,
                'company': data.newslistData.company,
                'reporter': data.newslistData.reporter,
                'datetime': data.newslistData.datetime
            })
    print(newslist_content)
    content = {
        'newslist_content': newslist_content
    }
    return render(request, 'newslist/index.html', content)
