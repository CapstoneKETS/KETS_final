from django.shortcuts import render
import requests
from bs4 import BeautifulSoup as bs
from django.http import HttpResponse


def index(request):
    return render(request, 'newslist/index.html')


# Create your views here.
