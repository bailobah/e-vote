# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from election import views
urlpatterns = [
    path('election/', views.election_list, name='election_list'),
    path('election/create/', views.election_create, name='election_create'),
    path('election/update/<int:pk>/', views.election_update, name='election_update'),
    path('election/delete/<int:pk>/', views.election_delete, name='election_delete'),
]