# Generated by Django 3.1.13 on 2022-06-28 12:21

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import users.functions
import users.mixins
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organizations', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('last_activity', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='last activity')),
                ('username', models.CharField(max_length=256, verbose_name='username')),
                ('email', models.EmailField(blank=True, max_length=254, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(blank=True, max_length=256, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=256, verbose_name='last name')),
                ('phone', models.CharField(blank=True, max_length=256, verbose_name='phone')),
                ('avatar', models.ImageField(blank=True, upload_to=users.functions.hash_upload)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether to treat this user as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('activity_at', models.DateTimeField(auto_now=True, verbose_name='last annotation activity')),
                ('active_organization', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='active_users', to='organizations.organization')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'db_table': 'htx_user',
            },
            bases=(users.mixins.UserMixin, models.Model),
            managers=[
                ('objects', users.models.UserManager()),
            ],
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['username'], name='htx_user_usernam_a41619_idx'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['email'], name='htx_user_email_051c68_idx'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['first_name'], name='htx_user_first_n_93c5de_idx'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['last_name'], name='htx_user_last_na_2ace53_idx'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['date_joined'], name='htx_user_date_jo_3bd95e_idx'),
        ),
    ]
