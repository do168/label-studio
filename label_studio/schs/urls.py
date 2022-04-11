"""This file and its contents are licensed under the Apache License 2.0. Please see the included NOTICE for copyright information and LICENSE for a copy of the license.
"""
from django.urls import include, path

from schs import api, views

app_name = 'schs'

# TODO: there should be only one patterns list based on API (with api/ prefix removed)
# Page URLs
_urlpatterns = [
    # get sch page
    path('', views.sch_people_list, name='sch-index'),
]

# API URLs
_api_urlpattens = [
    # sch list viewset
    path('', api.SchListAPI.as_view(), name='sch-index'),
    # sch detail viewset
    path('<int:pk>', api.SchAPI.as_view(), name='sch-detail'),
    # sch memberships list viewset
    path('<int:pk>/memberships', api.SchMemberListAPI.as_view(), name='sch-memberships-list'),
]

# TODO: these urlpatterns should be moved in core/urls with include('schs.urls')
urlpatterns = [
    path('sch/', views.simple_view, name='sch-simple'),
    path('sch/webhooks', views.simple_view, name='sch-simple'),

    path('people/', include(_urlpatterns)),
    path('api/schs/', include((_api_urlpattens, app_name), namespace='api')),
]
