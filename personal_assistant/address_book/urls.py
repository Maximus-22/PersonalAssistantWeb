from django.urls import path
from . import views
app_name = 'address_book'

urlpatterns = [
    # path('all_contacts/', views.all_contacts, name='all_contacts'),
    path('', views.contact_list, name='contact_list'),
    path('<int:page>', views.contact_list, name='contact_paginate'),
    path('contact_detail/<int:pk>/', views.contact_detail, name='contact_detail'),
    path('contact_add/', views.contact_add, name='contact_add'),
    path('contact_edit/<int:pk>/', views.contact_edit, name='contact_edit'),
    path('contact_delete/<int:pk>/', views.contact_delete, name='contact_delete'),
    path('upcoming_birthdays/', views.upcoming_birthdays, name='upcoming_birthdays'),
    path('contact_search/', views.contact_search, name='contact_search'),
]
