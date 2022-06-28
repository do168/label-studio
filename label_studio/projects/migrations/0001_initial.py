# Generated by Django 3.1.13 on 2022-06-28 12:21

import annoying.fields
import core.mixins
import core.utils.common
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='', help_text='Project name. Must be between 3 and 50 characters long.', max_length=50, null=True, validators=[django.core.validators.MinLengthValidator(3), django.core.validators.MaxLengthValidator(50)], verbose_name='title')),
                ('description', models.TextField(blank=True, default='', help_text='Project description', null=True, verbose_name='description')),
                ('label_config', models.TextField(blank=True, default='<View></View>', help_text='Label config in XML format. See more about it in documentation', null=True, verbose_name='label config')),
                ('expert_instruction', models.TextField(blank=True, default='', help_text='Labeling instructions in HTML format', null=True, verbose_name='expert instruction')),
                ('show_instruction', models.BooleanField(default=False, help_text='Show instructions to the annotator before they start', verbose_name='show instruction')),
                ('show_skip_button', models.BooleanField(default=True, help_text='Show a skip button in interface and allow annotators to skip the task', verbose_name='show skip button')),
                ('enable_empty_annotation', models.BooleanField(default=True, help_text='Allow annotators to submit empty annotations', verbose_name='enable empty annotation')),
                ('reveal_preannotations_interactively', models.BooleanField(default=False, help_text='Reveal pre-annotations interactively', verbose_name='reveal_preannotations_interactively')),
                ('show_annotation_history', models.BooleanField(default=False, help_text='Show annotation history to annotator', verbose_name='show annotation history')),
                ('show_collab_predictions', models.BooleanField(default=True, help_text='If set, the annotator can view model predictions', verbose_name='show predictions to annotator')),
                ('evaluate_predictions_automatically', models.BooleanField(default=False, help_text='Retrieve and display predictions when loading a task', verbose_name='evaluate predictions automatically')),
                ('token', models.CharField(blank=True, default=core.utils.common.create_hash, max_length=256, null=True, verbose_name='token')),
                ('result_count', models.IntegerField(default=0, help_text='Total results inside of annotations counter', verbose_name='result count')),
                ('color', models.CharField(blank=True, default='#FFFFFF', max_length=16, null=True, verbose_name='color')),
                ('maximum_annotations', models.IntegerField(default=1, help_text='Maximum number of annotations for one task. If the number of annotations per task is equal or greater to this value, the task is completed (is_labeled=True)', verbose_name='maximum annotation number')),
                ('min_annotations_to_start_training', models.IntegerField(default=10, help_text='Minimum number of completed tasks after which model training is started', verbose_name='min_annotations_to_start_training')),
                ('control_weights', models.JSONField(default=dict, help_text='Weights for control tags', null=True, verbose_name='control weights')),
                ('model_version', models.TextField(blank=True, default='', help_text='Machine learning model version', null=True, verbose_name='model version')),
                ('data_types', models.JSONField(default=dict, null=True, verbose_name='data_types')),
                ('is_draft', models.BooleanField(default=False, help_text='Whether or not the project is in the middle of being created', verbose_name='is draft')),
                ('is_published', models.BooleanField(default=False, help_text='Whether or not the project is published to annotators', verbose_name='published')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('sampling', models.CharField(choices=[('Sequential sampling', 'Tasks are ordered by Data manager ordering'), ('Uniform sampling', 'Tasks are chosen randomly'), ('Uncertainty sampling', 'Tasks are chosen according to model uncertainty scores (active learning mode)')], default='Sequential sampling', max_length=100, null=True)),
                ('show_ground_truth_first', models.BooleanField(default=False, verbose_name='show ground truth first')),
                ('show_overlap_first', models.BooleanField(default=False, verbose_name='show overlap first')),
                ('overlap_cohort_percentage', models.IntegerField(default=100, verbose_name='overlap_cohort_percentage')),
                ('task_data_login', models.CharField(blank=True, help_text='Task data credentials: login', max_length=256, null=True, verbose_name='task_data_login')),
                ('task_data_password', models.CharField(blank=True, help_text='Task data credentials: password', max_length=256, null=True, verbose_name='task_data_password')),
            ],
            options={
                'db_table': 'project',
            },
            bases=(core.mixins.DummyModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ProjectOnboardingSteps',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(choices=[('DU', 'Import your data'), ('CF', 'Configure settings'), ('PB', 'Publish project'), ('IE', 'Invite collaborators')], max_length=2, null=True)),
                ('title', models.CharField(max_length=1000, verbose_name='title')),
                ('description', models.TextField(verbose_name='description')),
                ('order', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='ProjectSummary',
            fields=[
                ('project', annoying.fields.AutoOneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='summary', serialize=False, to='projects.project')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Creation time', verbose_name='created at')),
                ('all_data_columns', models.JSONField(default=dict, help_text='All data columns found in imported tasks', null=True, verbose_name='all data columns')),
                ('common_data_columns', models.JSONField(default=list, help_text='Common data columns found across imported tasks', null=True, verbose_name='common data columns')),
                ('created_annotations', models.JSONField(default=dict, help_text='Unique annotation types identified by tuple (from_name, to_name, type)', null=True, verbose_name='created annotations')),
                ('created_labels', models.JSONField(default=dict, help_text='Unique labels', null=True, verbose_name='created labels')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectOnboarding',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('finished', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
                ('step', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='po_through', to='projects.projectonboardingsteps')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enabled', models.BooleanField(default=True, help_text='Project member is enabled')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('project', models.ForeignKey(help_text='Project ID', on_delete=django.db.models.deletion.CASCADE, related_name='members', to='projects.project')),
            ],
        ),
    ]
