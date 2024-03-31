from . import views
from django.urls import path

app_name = 'mainpage'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:kwRank_keyword>/', views.newsList, name='newsList'),  # /news/ URL에 대한 newsList 뷰 매핑
    path('<str:kwRank_keyword>/<int:newsData_id>/', views.details, name='details'),  # /details/ URL에 대한 details 뷰 매핑
]