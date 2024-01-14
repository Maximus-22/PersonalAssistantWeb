from django.urls import path

from . import views

app_name = 'news'
urlpatterns = [
    path('', views.all_news, name='main_news'),
    path('ukr/', views.ukraine_news, name='ukraine_news'),
    path('finance/', views.finance_news, name='finance_news'),
    path('culture/', views.culture_news, name='culture_news'),
    path('sport/', views.sport_news, name='sport_news'),
]