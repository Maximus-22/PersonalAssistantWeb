from django.urls import path

from . import views

app_name = 'address_book'
urlpatterns = [
    path('', views.all_contacts, name='all_contacts'),
]