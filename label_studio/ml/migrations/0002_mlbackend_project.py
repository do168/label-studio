# Generated by Django 3.1.13 on 2022-06-28 12:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
        ('ml', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mlbackend',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ml_backends', to='projects.project'),
        ),
    ]
