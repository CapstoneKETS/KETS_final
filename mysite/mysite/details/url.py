from django.urls import path

from . import views
app_name = 'details'
urlpatterns = [
    path('', views.index, name='index')
]