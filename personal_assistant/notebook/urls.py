from django.urls import path

from . import views

app_name = 'notebook'
urlpatterns = [
    path('', views.all_notes, name='all_notes'),
]