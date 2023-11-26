from django.urls import path

from . import views
app_name = 'newslist'

urlpatterns = [
    path('', views.index, name='index')
]