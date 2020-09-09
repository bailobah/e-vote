# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.conf.urls import url
from django.db import router
from django.urls import path, include
from  django.conf.urls.static import static
from .views import login_view, register_user
from django.contrib.auth.views import LogoutView

from django.conf import settings
from election import views
from political_party import views as views_party
from locality_type import views as l_views
from api import views as api_views
from rest_framework import routers
router = routers.DefaultRouter()

l_name = 'locality_type'


urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),

    path('election/', views.election_list, name='election_list'),
    path('election/create/', views.election_create, name='election_create'),
    path('election/update/<int:pk>/', views.election_update, name='election_update'),
    path('election/delete/<int:pk>/', views.election_delete, name='election_delete'),

    path('political_party/', views_party.political_party_list, name='political_party_list'),
    path('political_party/create/', views_party.political_party_create, name='political_party_create'),
    path('political_party/update/<int:pk>/', views_party.political_party_update, name='political_party_update'),
    path('political_party/delete/<int:pk>/', views_party.political_party_delete, name='political_party_delete'),

    path('locality_type/', l_views.locality_type_list, name=f'{l_name}_list'),
    path('locality_type/create/', l_views.locality_type_create, name=f'{l_name}_create'),
    path('locality_type/update/<int:pk>/', l_views.locality_type_update, name=f'{l_name}_update'),
    path('locality_type/delete/<int:pk>/', l_views.locality_type_delete, name=f'{l_name}_delete'),

    path('minute/', views.minute_list, name='minute_list'),
    path('minute/create/', views.minute_create, name='minute_create'),
    path('minute/update/<int:pk>/', views.minute_update, name='minute_update'),
    path('minute/delete/<int:pk>/', views.minute_delete, name='minute_delete'),
    #url(r'^api/', include('rest_framework.urls', namespace='rest_framework')),
    #url(r'^api/', include(router.urls)),
    path('api/v1/', include('rest_auth.urls')),
    path('api/v1/getdata/', api_views.get_data),
    path('api/v1/account/', include('allauth.urls')),
    #url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)