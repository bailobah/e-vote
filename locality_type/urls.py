# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present Sabinnov
"""

from django.urls import path


from locality_type import views as l_views

name = 'locality_type'

urlpatterns = [

    path(f'{name}/', l_views.locality_type_list, name=f'{name}_list'),
    path(f'{name}/create/', l_views.locality_type_create, name=f'{name}_create'),
    path(f'{name}/update/<int:pk>/', l_views.locality_type_update, name=f'{name}_update'),
    path(f'{name}/delete/<int:pk>/', l_views.locality_type_delete, name=f'{name}_delete'),

]
