from django.urls import path

from . import views

app_name = 'file_storage'
urlpatterns = [
    path('', views.all_files, name='all_files'),
]