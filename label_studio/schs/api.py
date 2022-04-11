"""This file and its contents are licensed under the Apache License 2.0. Please see the included NOTICE for copyright information and LICENSE for a copy of the license.
"""
import logging

from django.urls import reverse
from django.conf import settings
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils.decorators import method_decorator

from label_studio.core.permissions import all_permissions, ViewClassPermission
from label_studio.core.utils.common import get_object_with_check_and_log, bool_from_request

from schs.models import Sch
from schs.serializers import (
    SchSerializer, SchIdSerializer, SchMemberUserSerializer, SchInviteSerializer
)


logger = logging.getLogger(__name__)


@method_decorator(name='get', decorator=swagger_auto_schema(
        tags=['Schs'],
        operation_summary='List your schs',
        operation_description="""
        Return a list of the schs you've created or that you have access to.
        """
    ))
class SchListAPI(generics.ListCreateAPIView):
    queryset = Sch.objects.all()
    parser_classes = (JSONParser, FormParser, MultiPartParser)
    permission_required = ViewClassPermission(
        GET=all_permissions.schs_view,
        PUT=all_permissions.schs_change,
        POST=all_permissions.schs_create,
        PATCH=all_permissions.schs_change,
        DELETE=all_permissions.schs_change,
    )
    serializer_class = SchIdSerializer

    def get_object(self):
        org = get_object_with_check_and_log(self.request, Sch, pk=self.kwargs[self.lookup_field])
        self.check_object_permissions(self.request, org)
        return org

    def filter_queryset(self, queryset):
        return queryset.filter(users=self.request.user).distinct()

    def get(self, request, *args, **kwargs):
        return super(SchListAPI, self).get(request, *args, **kwargs)

    @swagger_auto_schema(auto_schema=None)
    def post(self, request, *args, **kwargs):
        return super(SchListAPI, self).post(request, *args, **kwargs)


class SchMemberPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'

    def get_page_size(self, request):
        # emulate "unlimited" page_size
        if self.page_size_query_param in request.query_params and request.query_params[self.page_size_query_param] == '-1':
            return 1000000
        return super().get_page_size(request)


@method_decorator(name='get', decorator=swagger_auto_schema(
        tags=['Schs'],
        operation_summary='Get schs members list',
        operation_description='Retrieve a list of the schs members and their IDs.',
        manual_parameters=[
            openapi.Parameter(
                name='id',
                type=openapi.TYPE_INTEGER,
                in_=openapi.IN_PATH,
                description='A unique integer value identifying this schs.'),
        ],
    ))
class SchMemberListAPI(generics.ListAPIView):

    parser_classes = (JSONParser, FormParser, MultiPartParser)
    permission_required = ViewClassPermission(
        GET=all_permissions.schs_view,
        PUT=all_permissions.schs_change,
        PATCH=all_permissions.schs_change,
        DELETE=all_permissions.schs_change,
    )
    serializer_class = SchMemberUserSerializer
    pagination_class = SchMemberPagination

    def get_serializer_context(self):
        return {
            'contributed_to_projects': bool_from_request(self.request.GET, 'contributed_to_projects', False)
        }

    def get_queryset(self):
        org = generics.get_object_or_404(self.request.user.schs, pk=self.kwargs[self.lookup_field])
        return org.members.order_by('user__username')


@method_decorator(name='get', decorator=swagger_auto_schema(
        tags=['Schs'],
        operation_summary=' Get schs settings',
        operation_description='Retrieve the settings for a specific schs by ID.'
    ))
@method_decorator(name='patch', decorator=swagger_auto_schema(
        tags=['Schs'],
        operation_summary='Update schs settings',
        operation_description='Update the settings for a specific schs by ID.'
    ))
class SchAPI(generics.RetrieveUpdateAPIView):

    parser_classes = (JSONParser, FormParser, MultiPartParser)
    queryset = Sch.objects.all()
    permission_required = all_permissions.schs_change
    serializer_class = SchSerializer

    redirect_route = 'schs-dashboard'
    redirect_kwarg = 'pk'

    def get_object(self):
        org = generics.get_object_or_404(self.request.user.schs, pk=self.kwargs[self.lookup_field])
        self.check_object_permissions(self.request, org)
        return org

    def get(self, request, *args, **kwargs):
        return super(SchAPI, self).get(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return super(SchAPI, self).patch(request, *args, **kwargs)

    @swagger_auto_schema(auto_schema=None)
    def post(self, request, *args, **kwargs):
        return super(SchAPI, self).post(request, *args, **kwargs)

    @swagger_auto_schema(auto_schema=None)
    def put(self, request, *args, **kwargs):
        return super(SchAPI, self).put(request, *args, **kwargs)