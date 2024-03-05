from django.shortcuts import render

# from .models import kwRank

def index(request):
    # queryset = kwRank.objects.order_by('-rank')[:16]
    #
    # keyword_list = [obj.keyword for obj in queryset]
    #
    # context = {
    #     'keyword_list': keyword_list,
    # }

    return render(request, 'mainpage/index.html')

# Create your views here.
