from . import views
from django.urls import path

app_name = 'mainpage'

urlpatterns = [
    path('', views.index, name='index')
]