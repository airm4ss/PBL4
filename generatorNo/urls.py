# generatorNo/urls.py

from django.urls import path
from . import views

app_name = 'generatorNo'

urlpatterns = [
    path('generatorNo_home/', views.gen_no_home, name='generatorNo_home'),
    path('generatorNo/result/', views.no_preview_html, name='generatorNo_result'),
    path('create/', views.create, name='create'),
    path('qr_preview/', views.qr_preview, name='qr_preview'),
    path('download_qr_image/', views.download_qr_image, name='download_qr_image'),
]
