"""This file and its contents are licensed under the Apache License 2.0. Please see the included NOTICE for copyright information and LICENSE for a copy of the license.
"""

from .models import Sch, SchMember


from django.forms import Textarea, ModelForm, TextInput, Form, FileField, Select, HiddenInput, CharField


class SchForm(ModelForm):
    """
    """
    org_update = CharField(widget=HiddenInput(), required=False)
    
    class Meta:
        model = Sch
        fields = ('title',)


class SchSignupForm(ModelForm):
    """
    """
    class Meta:
        model = Sch
        fields = ('title',)
