# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.conf.urls import url
from django.db import router
from django.urls import path, include
from  django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token

from api.views import PollingList, PollingDetails, Login, inbound_sms, PollingDetail
from .views import login_view, register_user
from django.contrib.auth.views import LogoutView

from django.conf import settings
from election import views
from sms import views as s_views
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

    path('sms/', s_views.sms_list, name=f'sms_list'),
    path('sms/delete/<int:pk>/', s_views.sms_delete, name='sms_delete'),

    path('locality_type/', l_views.locality_type_list, name=f'{l_name}_list'),
    path('locality_type/create/', l_views.locality_type_create, name=f'{l_name}_create'),
    path('locality_type/update/<int:pk>/', l_views.locality_type_update, name=f'{l_name}_update'),
    path('locality_type/delete/<int:pk>/', l_views.locality_type_delete, name=f'{l_name}_delete'),


    path('minute/', views.minute_list, name='minute_list'),
    path('minute/create/', views.MinuteCreate.as_view(), name='minute_create'),
    path('minute/update/<int:pk>/', views.MinuteUpdate.as_view(), name='minute_update'),
    path('minute/delete/<int:pk>/', views.minute_delete, name='minute_delete'),
    path('minute_detail/<int:pk>/', views.minute_detail, name='minute_detail'),
    path('api/v1/polling/', PollingList.as_view()),
    path('api/v1/polling_detail/', PollingDetails.as_view()),
    path('api/v1/find_minute/', PollingDetail.as_view()),

    path('api/v1/polling_detail/<int:pk>/', PollingDetails.as_view()),
    path('api/v1/evote-sms/', inbound_sms, name='inbound_sms'),
    #path('api/v1/account/', include('allauth.urls')),
    path('api/v1/login/', Login.as_view(), name='api_token_auth'),
    #url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
