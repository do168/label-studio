# Generated by Django 3.1.13 on 2022-04-05 04:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('schs', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='schmember',
            name='user',
            field=models.ForeignKey(help_text='User ID', on_delete=django.db.models.deletion.CASCADE, related_name='sm_through', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='sch',
            name='created_by',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sch', to=settings.AUTH_USER_MODEL, verbose_name='created_by'),
        ),
        migrations.AddField(
            model_name='sch',
            name='users',
            field=models.ManyToManyField(related_name='schs', through='schs.SchMember', to=settings.AUTH_USER_MODEL),
        ),
    ]
