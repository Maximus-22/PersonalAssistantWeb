from django.urls import path

from . import views

app_name = 'file_storage'
urlpatterns = [
    path('', views.all_files, name='all_files'),
    path('upload/', views.file_upload_view, name='file-upload'),
    path('delete/<int:file_id>/', views.delete_file, name='delete-file'),
]