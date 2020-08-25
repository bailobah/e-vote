# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path


from political_party import views
urlpatterns = [

    path('political_party/', views.political_party_list, name='political_party_list'),
    path('political_party/create/', views.political_party_create, name='political_party_create'),
    path('political_party/update/<int:pk>/', views.political_party_update, name='political_party_update'),
    path('political_party/delete/<int:pk>/', views.political_party_delete, name='political_party_delete'),

]
