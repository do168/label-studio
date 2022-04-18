"""This file and its contents are licensed under the Apache License 2.0. Please see the included NOTICE for copyright information and LICENSE for a copy of the license.
"""
import logging

from django.db import models, transaction
from django.conf import settings
from django.db.models import Q, Count

from django.utils.translation import gettext_lazy as _

from core.utils.common import create_hash, get_object_with_check_and_log, load_func

logger = logging.getLogger(__name__)

# TODO: create SCH_MIXIN as PROJECT_MIXIN
SchMixin = load_func(settings.SCH_MIXIN)


class Sch(SchMixin, models.Model):
    title = models.CharField(
        _('sch title'),
        max_length=1000,
        null=False,
    )
    organization = models.ForeignKey(
        'organizations.Organization', on_delete=models.CASCADE, related_name='schs', null=True
    )
    dataset = models.CharField(
        _('sch dataset'),
        max_length=1000,
        null=False,
    )
    inf_model = models.CharField(
        _('sch inference model'),
        max_length=1000,
        null=False,
    )
    period = models.CharField(
        _('sch period'),
        max_length=1000,
        null=False,
    )
    tmp_auto_remove = models.BooleanField(
        _('sch temp auto removed'),
        default=False,
    )
    prj_auto_create = models.BooleanField(
        _('sch prj auto created'),
        default=False,
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='created_sch',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('created by'),
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    def created_at_prettify(self):
        return self.created_at.strftime("%d %b %Y %H:%M:%S")

    def save(self, *args, recalc=True, **kwargs):
        super(Sch, self).save(*args, **kwargs)

    @staticmethod
    def django_settings():
        return settings

    def __str__(self):
        return self.title + ', id=' + str(self.pk)


class SchMember(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sch_memberships', help_text='User ID'
    )  # noqa
    sch = models.ForeignKey(Sch, on_delete=models.CASCADE, related_name='members', help_text='Project ID')
    enabled = models.BooleanField(default=True, help_text='Sch member is enabled')
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)