from django.urls import path

from .views import *

app_name = 'notebook'

urlpatterns = [
    path('', notebook_list, name='all_notes'),
    path('<int:page>', notebook_list, name='all_notes_paginate'),
    path('add_note/', add_note, name='add_note'),
    path('search/', search_notes, name='search_notes'),
    path('update_note/<int:notebook_id>/', update_note, name='update_note'),
    path('delete_note/<int:notebook_id>/', delete_note, name='delete_note'),
    path('tag/<str:tag_name>/', TagNotesView.as_view(), name='tag_notes'),
]