from django.http import HttpResponse
from django.shortcuts import render
# from .models import newsData

def index(request):
    # details = newsData.objects
    #미완성. newsData에서 요약문을 가져올 방법을 찾는 중입니다.
    return render(request, 'details/index.html')
