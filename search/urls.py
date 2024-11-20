from django.urls import path
from . import views

app_name = 'search'

urlpatterns = [
    path('', views.search_hospital, name='search_hospital'),  # 검색 페이지
    path('hospital/<int:id>/', views.hospital_detail, name='hospital_detail'),  # 병원 세부 정보 페이지
]
