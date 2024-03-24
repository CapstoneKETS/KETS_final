from django.shortcuts import render
import random
from .models import kwRank

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
