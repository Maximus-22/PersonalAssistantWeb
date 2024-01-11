from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main, name='main'),
    path('auth/', include('accounts.urls')),
    path('contacts/', include('address_book.urls')),
    path('notes/', include('notebook.urls')),
    path('files/', include('file_storage.urls')),
    path('news/', include('news.urls')),
]
