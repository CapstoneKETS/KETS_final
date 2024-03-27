from . import views
from django.urls import path

app_name = 'mainpage'

urlpatterns = [
    path('', views.index, name='index'),
    path('newslist/', views.newsList, name='news_list'),  # /news/ URL에 대한 newsList 뷰 매핑
    path('details/', views.details, name='details'),  # /details/ URL에 대한 details 뷰 매핑
]