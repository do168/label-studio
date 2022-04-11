"""This file and its contents are licensed under the Apache License 2.0. Please see the included NOTICE for copyright information and LICENSE for a copy of the license.
"""
import logging

from django.db import models, transaction
from django.conf import settings
from django.db.models import Q, Count

from django.utils.translation import gettext_lazy as _

from core.utils.common import create_hash, get_object_with_check_and_log, get_sch_from_request, load_func

logger = logging.getLogger(__name__)


class SchMember(models.Model):
    """
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sm_through',
        help_text='User ID'
    )
    sch = models.ForeignKey(
        'schs.Sch', on_delete=models.CASCADE,
        help_text='Sch ID'
    )
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    @classmethod
    def find_by_user(cls, user_or_user_pk, sch_pk):
        from users.models import User

        user_pk = user_or_user_pk.pk if isinstance(user_or_user_pk, User) else user_or_user_pk
        return SchMember.objects.get(user=user_pk, sch=sch_pk)

    @property
    def is_owner(self):
        return self.user.id == self.sch.created_by.id

    class Meta:
        ordering = ['pk']


SchMixin = load_func(settings.SCH_MIXIN)


class Sch(SchMixin, models.Model):
    """
    """
    title = models.CharField(_('sch title'), max_length=1000, null=False)

    # dataset = models.CharField(_('sch dataset'), max_length=1000, null=False)

    # token = models.CharField(_('token'), max_length=256, default=create_hash, unique=True, null=True, blank=True)

    # inference_model = models.CharField(_('inference model'), max_length=100, null=False)
    #
    # period = models.CharField(_('period'), max_length=100, null=False)
    #
    # tmp_auto_remove = models.BooleanField(_('tmp_auto_remove'), default=False)
    #
    # project_auto_create = models.BooleanField(_('project_auto_create'), default=False)

    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="schs", through=SchMember)
        
    created_by = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                      null=True, related_name="sch", verbose_name=_('created_by'))

    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    def __str__(self):
        return self.title + ', id=' + str(self.pk)

    @classmethod
    def from_request(cls, request):
        if 'sch_pk' not in request.session:
            logger.debug('"sch_pk" is missed in request.session: can\'t get Sch')
            return
        pk = get_sch_from_request(request)
        return get_object_with_check_and_log(request, Sch, pk=pk)

    @classmethod
    def create_sch(cls, created_by=None, title='Your Sch'):
        _create_sch = load_func(settings.CREATE_SCH)
        return _create_sch(title=title, created_by=created_by)
    
    @classmethod
    def find_by_user(cls, user):
        memberships = SchMember.objects.filter(user=user).prefetch_related('sch')
        if not memberships.exists():
            raise ValueError(f'No memberships found for user {user}')
        return memberships.first().sch

    # @classmethod
    # def find_by_invite_url(cls, url):
    #     token = url.strip('/').split('/')[-1]
    #     if len(token):
    #         return Sch.objects.get(token=token)
    #     else:
    #         raise KeyError(f'Can\'t find Sch by welcome URL: {url}')

    def has_user(self, user):
        return self.users.filter(pk=user.pk).exists()

    def has_project_member(self, user):
        return self.projects.filter(members__user=user).exists()

    def has_permission(self, user):
        if self in user.schs.all():
            return True
        return False

    def add_user(self, user):
        if self.users.filter(pk=user.pk).exists():
            logger.debug('User already exists in sch.')
            return

        with transaction.atomic():
            om = SchMember(user=user, sch=self)
            om.save()

            return om    
    
    def check_max_projects(self):
        """This check raise an exception if the projects limit is hit
        """
        pass

    def projects_sorted_by_created_at(self):
        return self.projects.all().order_by('-created_at').annotate(
            tasks_count=Count('tasks'),
            labeled_tasks_count=Count('tasks', filter=Q(tasks__is_labeled=True))
        ).prefetch_related('created_by')

    def created_at_prettify(self):
        return self.created_at.strftime("%d %b %Y %H:%M:%S")

    def per_project_invited_users(self):
        from users.models import User

        invited_ids = self.projects.values_list('members__user__pk', flat=True).distinct()
        per_project_invited_users = User.objects.filter(pk__in=invited_ids)
        return per_project_invited_users

    @property
    def secure_mode(self):
        return False

    @property
    def members(self):
        return SchMember.objects.filter(sch=self)

    class Meta:
        db_table = 'sch'
