from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.views.decorators.cache import cache_control
from django.contrib.staticfiles.views import serve

from . import views
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main, name='main'),
    path('auth/', include('accounts.urls')),
    path('contacts/', include('address_book.urls')),
    path('notes/', include('notebook.urls')),
    path('files/', include('file_storage.urls')),
    path('news/', include('news.urls')),
    path('pomodoro/', include('pomodoro.urls')),
] + static(settings.STATIC_URL, view=cache_control(no_cache=True, must_revalidate=True)(serve))
