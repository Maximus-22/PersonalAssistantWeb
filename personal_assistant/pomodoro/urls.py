from django.urls import path
from . import views

app_name = 'pomodoro'


urlpatterns = [
    path('', views.index, name='pomodoro'),
    path('start/<str:session_type>/', views.start_pomodoro, name='start_pomodoro'),
]
