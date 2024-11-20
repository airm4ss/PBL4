# home/urls.py
from django.urls import path,include
from django.contrib import admin
from . import views
from .views import index

app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),
    path('generatorHave/', views.generatorHave, name='generatorHave'),
    path('generatorNo/', views.generatorNo, name='generatorNo'),
    
]
