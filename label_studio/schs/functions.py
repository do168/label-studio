from django.db import transaction

from core.utils.common import temporary_disconnect_all_signals
from schs.models import Sch, SchMember
from projects.models import Project


def create_sch(title, created_by):
    with transaction.atomic():
        org = Sch.objects.create(title=title, created_by=created_by)
        SchMember.objects.create(user=created_by, sch=org)
        return org


def destroy_sch(org):
    with temporary_disconnect_all_signals():
        Project.objects.filter(sch=org).delete()
        org.delete()
