"""This file and its contents are licensed under the Apache License 2.0. Please see the included NOTICE for copyright information and LICENSE for a copy of the license.
"""
import ujson as json

from rest_framework import serializers
from drf_dynamic_fields import DynamicFieldsMixin

from schs.models import Sch, SchMember
from users.serializers import UserSimpleSerializer
from collections import OrderedDict


class CreatedByFromContext:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context.get('created_by')


class SchSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    created_by = UserSimpleSerializer(default=CreatedByFromContext())

    class Meta:
        model = Sch
        fields = '__all__'
