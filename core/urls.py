# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present Sabinnov
"""
from django.conf.urls import url
from django.contrib import admin

from django.urls import path, include  # add this
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),          # Django admin route
    path("", include("authentication.urls")), # Auth routes - login / register
    path("", include("app.urls")),            # UI Kits Html files
    #url(r'^api/', include(router.urls)),
    #path("", include("election.urls")) ,           # UI Kits Html files
    #path("political_party", include("political_party.urls"), name='party') ,           # UI Kits Html files
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)