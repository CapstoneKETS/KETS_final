from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'details/index.html')
# Create your views here.
