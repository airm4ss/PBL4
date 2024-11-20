from django.urls import path
from . import views

app_name = 'generatorHave'

urlpatterns = [
    path('genHave_home/', views.gen_have_home, name='genHave_home'),
    path('genHave/result/', views.yes_preview_html, name='genHave_result'),
]
