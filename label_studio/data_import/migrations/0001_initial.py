# Generated by Django 3.1.13 on 2022-05-25 06:09

import data_import.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FileUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=data_import.models.upload_name_generator)),
            ],
        ),
    ]
