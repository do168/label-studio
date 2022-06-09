# Generated by Django 3.1.13 on 2022-05-25 06:09

import core.mixins
import core.utils.common
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000, verbose_name='organization title')),
                ('token', models.CharField(blank=True, default=core.utils.common.create_hash, max_length=256, null=True, unique=True, verbose_name='token')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
            ],
            options={
                'db_table': 'organization',
            },
            bases=(core.mixins.DummyModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='OrganizationMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('organization', models.ForeignKey(help_text='Organization ID', on_delete=django.db.models.deletion.CASCADE, to='organizations.organization')),
            ],
            options={
                'ordering': ['pk'],
            },
        ),
    ]
