# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from .views import login_view, register_user
from django.contrib.auth.views import LogoutView
from users.views import update_profile

from election import views
from political_party import views as views_party
urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('profile/', update_profile, name="update_profile"),
    path('election/', views.election_list, name='election_list'),
    path('election/create/', views.election_create, name='election_create'),
    path('election/update/<int:pk>/', views.election_update, name='election_update'),
    path('election/delete/<int:pk>/', views.election_delete, name='election_delete'),

    path('political_party/', views_party.political_party_list, name='political_party_list'),
    path('political_party/create/', views_party.political_party_create, name='political_party_create'),
    path('political_party/update/<int:pk>/', views_party.political_party_update, name='political_party_update'),
    path('political_party/delete/<int:pk>/', views_party.political_party_delete, name='political_party_delete'),

]
