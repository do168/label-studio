# Generated by Django 3.1.13 on 2022-04-05 04:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MLBackend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(choices=[('CO', 'Connected'), ('DI', 'Disconnected'), ('ER', 'Error'), ('TR', 'Training'), ('PR', 'Predicting')], default='DI', max_length=2)),
                ('is_interactive', models.BooleanField(default=False, help_text='Used to interactively annotate tasks. If true, model returns one list with results', verbose_name='is_interactive')),
                ('url', models.TextField(help_text='URL for the machine learning model server', verbose_name='url')),
                ('error_message', models.TextField(blank=True, help_text='Error message in error state', null=True, verbose_name='error_message')),
                ('title', models.TextField(blank=True, default='default', help_text='Name of the machine learning backend', null=True, verbose_name='title')),
                ('description', models.TextField(blank=True, default='', help_text='Description for the machine learning backend', null=True, verbose_name='description')),
                ('model_version', models.TextField(blank=True, default='', help_text='Current model version associated with this machine learning backend', null=True, verbose_name='model version')),
                ('timeout', models.FloatField(blank=True, default=100.0, help_text='Response model timeout', verbose_name='timeout')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
            ],
        ),
        migrations.CreateModel(
            name='MLBackendTrainJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_id', models.CharField(max_length=128)),
                ('model_version', models.TextField(blank=True, help_text='Model version this job is associated with', null=True, verbose_name='model version')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('ml_backend', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='train_jobs', to='ml.mlbackend')),
            ],
        ),
        migrations.CreateModel(
            name='MLBackendPredictionJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_id', models.CharField(max_length=128)),
                ('model_version', models.TextField(blank=True, help_text='Model version this job is associated with', null=True, verbose_name='model version')),
                ('batch_size', models.PositiveSmallIntegerField(default=100, help_text='Number of tasks processed per batch', verbose_name='batch size')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('ml_backend', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prediction_jobs', to='ml.mlbackend')),
            ],
        ),
    ]
