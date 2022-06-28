# Generated by Django 3.1.13 on 2022-06-28 12:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AzureBlobExportStorageLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_exists', models.BooleanField(default=True, help_text='Whether object under external link still exists', verbose_name='object exists')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Creation time', verbose_name='created at')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AzureBlobImportStorageLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.TextField(help_text='External link key', verbose_name='key')),
                ('object_exists', models.BooleanField(default=True, help_text='Whether object under external link still exists', verbose_name='object exists')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Creation time', verbose_name='created at')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AzureBlobStorageMixin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('container', models.TextField(blank=True, help_text='Azure blob container', null=True, verbose_name='container')),
                ('prefix', models.TextField(blank=True, help_text='Azure blob prefix name', null=True, verbose_name='prefix')),
                ('regex_filter', models.TextField(blank=True, help_text='Cloud storage regex for filtering objects', null=True, verbose_name='regex_filter')),
                ('use_blob_urls', models.BooleanField(default=False, help_text='Interpret objects as BLOBs and generate URLs', verbose_name='use_blob_urls')),
                ('account_name', models.TextField(blank=True, help_text='Azure Blob account name', null=True, verbose_name='account_name')),
                ('account_key', models.TextField(blank=True, help_text='Azure Blob account key', null=True, verbose_name='account_key')),
            ],
        ),
        migrations.CreateModel(
            name='GCSExportStorageLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_exists', models.BooleanField(default=True, help_text='Whether object under external link still exists', verbose_name='object exists')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Creation time', verbose_name='created at')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GCSImportStorageLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.TextField(help_text='External link key', verbose_name='key')),
                ('object_exists', models.BooleanField(default=True, help_text='Whether object under external link still exists', verbose_name='object exists')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Creation time', verbose_name='created at')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GCSStorageMixin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bucket', models.TextField(blank=True, help_text='GCS bucket name', null=True, verbose_name='bucket')),
                ('prefix', models.TextField(blank=True, help_text='GCS bucket prefix', null=True, verbose_name='prefix')),
                ('regex_filter', models.TextField(blank=True, help_text='Cloud storage regex for filtering objects', null=True, verbose_name='regex_filter')),
                ('use_blob_urls', models.BooleanField(default=False, help_text='Interpret objects as BLOBs and generate URLs', verbose_name='use_blob_urls')),
                ('google_application_credentials', models.TextField(blank=True, help_text='The content of GOOGLE_APPLICATION_CREDENTIALS json file', null=True, verbose_name='google_application_credentials')),
            ],
        ),
        migrations.CreateModel(
            name='LocalFilesExportStorageLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_exists', models.BooleanField(default=True, help_text='Whether object under external link still exists', verbose_name='object exists')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Creation time', verbose_name='created at')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LocalFilesImportStorageLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.TextField(help_text='External link key', verbose_name='key')),
                ('object_exists', models.BooleanField(default=True, help_text='Whether object under external link still exists', verbose_name='object exists')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Creation time', verbose_name='created at')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LocalFilesMixin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.TextField(blank=True, help_text='Local path', null=True, verbose_name='path')),
                ('regex_filter', models.TextField(blank=True, help_text='Regex for filtering objects', null=True, verbose_name='regex_filter')),
                ('use_blob_urls', models.BooleanField(default=False, help_text='Interpret objects as BLOBs and generate URLs', verbose_name='use_blob_urls')),
            ],
        ),
        migrations.CreateModel(
            name='RedisExportStorageLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_exists', models.BooleanField(default=True, help_text='Whether object under external link still exists', verbose_name='object exists')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Creation time', verbose_name='created at')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RedisImportStorageLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.TextField(help_text='External link key', verbose_name='key')),
                ('object_exists', models.BooleanField(default=True, help_text='Whether object under external link still exists', verbose_name='object exists')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Creation time', verbose_name='created at')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RedisStorageMixin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.TextField(blank=True, help_text='Storage prefix (optional)', null=True, verbose_name='path')),
                ('host', models.TextField(blank=True, help_text='Server Host IP (optional)', null=True, verbose_name='host')),
                ('port', models.TextField(blank=True, help_text='Server Port (optional)', null=True, verbose_name='port')),
                ('password', models.TextField(blank=True, help_text='Server Password (optional)', null=True, verbose_name='password')),
                ('regex_filter', models.TextField(blank=True, help_text='Cloud storage regex for filtering objects', null=True, verbose_name='port')),
                ('use_blob_urls', models.BooleanField(default=False, help_text='Interpret objects as BLOBs and generate URLs', verbose_name='use_blob_urls')),
            ],
        ),
        migrations.CreateModel(
            name='S3ExportStorage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, help_text='Cloud storage title', max_length=256, null=True, verbose_name='title')),
                ('description', models.TextField(blank=True, help_text='Cloud storage description', null=True, verbose_name='description')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Creation time', verbose_name='created at')),
                ('last_sync', models.DateTimeField(blank=True, help_text='Last sync finished time', null=True, verbose_name='last sync')),
                ('last_sync_count', models.PositiveIntegerField(blank=True, help_text='Count of tasks synced last time', null=True, verbose_name='last sync count')),
                ('can_delete_objects', models.BooleanField(blank=True, help_text='Deletion from storage enabled', null=True, verbose_name='can_delete_objects')),
                ('bucket', models.TextField(blank=True, help_text='S3 bucket name', null=True, verbose_name='bucket')),
                ('prefix', models.TextField(blank=True, help_text='S3 bucket prefix', null=True, verbose_name='prefix')),
                ('regex_filter', models.TextField(blank=True, help_text='Cloud storage regex for filtering objects', null=True, verbose_name='regex_filter')),
                ('use_blob_urls', models.BooleanField(default=False, help_text='Interpret objects as BLOBs and generate URLs', verbose_name='use_blob_urls')),
                ('aws_access_key_id', models.TextField(blank=True, help_text='AWS_ACCESS_KEY_ID', null=True, verbose_name='aws_access_key_id')),
                ('aws_secret_access_key', models.TextField(blank=True, help_text='AWS_SECRET_ACCESS_KEY', null=True, verbose_name='aws_secret_access_key')),
                ('aws_session_token', models.TextField(blank=True, help_text='AWS_SESSION_TOKEN', null=True, verbose_name='aws_session_token')),
                ('region_name', models.TextField(blank=True, help_text='AWS Region', null=True, verbose_name='region_name')),
                ('s3_endpoint', models.TextField(blank=True, help_text='S3 Endpoint', null=True, verbose_name='s3_endpoint')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='S3ExportStorageLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_exists', models.BooleanField(default=True, help_text='Whether object under external link still exists', verbose_name='object exists')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Creation time', verbose_name='created at')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='S3ImportStorage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, help_text='Cloud storage title', max_length=256, null=True, verbose_name='title')),
                ('description', models.TextField(blank=True, help_text='Cloud storage description', null=True, verbose_name='description')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Creation time', verbose_name='created at')),
                ('last_sync', models.DateTimeField(blank=True, help_text='Last sync finished time', null=True, verbose_name='last sync')),
                ('last_sync_count', models.PositiveIntegerField(blank=True, help_text='Count of tasks synced last time', null=True, verbose_name='last sync count')),
                ('bucket', models.TextField(blank=True, help_text='S3 bucket name', null=True, verbose_name='bucket')),
                ('prefix', models.TextField(blank=True, help_text='S3 bucket prefix', null=True, verbose_name='prefix')),
                ('regex_filter', models.TextField(blank=True, help_text='Cloud storage regex for filtering objects', null=True, verbose_name='regex_filter')),
                ('use_blob_urls', models.BooleanField(default=False, help_text='Interpret objects as BLOBs and generate URLs', verbose_name='use_blob_urls')),
                ('aws_access_key_id', models.TextField(blank=True, help_text='AWS_ACCESS_KEY_ID', null=True, verbose_name='aws_access_key_id')),
                ('aws_secret_access_key', models.TextField(blank=True, help_text='AWS_SECRET_ACCESS_KEY', null=True, verbose_name='aws_secret_access_key')),
                ('aws_session_token', models.TextField(blank=True, help_text='AWS_SESSION_TOKEN', null=True, verbose_name='aws_session_token')),
                ('region_name', models.TextField(blank=True, help_text='AWS Region', null=True, verbose_name='region_name')),
                ('s3_endpoint', models.TextField(blank=True, help_text='S3 Endpoint', null=True, verbose_name='s3_endpoint')),
                ('presign', models.BooleanField(default=True, help_text='Generate presigned URLs', verbose_name='presign')),
                ('presign_ttl', models.PositiveSmallIntegerField(default=1, help_text='Presigned URLs TTL (in minutes)', verbose_name='presign_ttl')),
                ('recursive_scan', models.BooleanField(default=False, help_text='Perform recursive scan over the bucket content', verbose_name='recursive scan')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AzureBlobExportStorage',
            fields=[
                ('azureblobstoragemixin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='io_storages.azureblobstoragemixin')),
                ('title', models.CharField(blank=True, help_text='Cloud storage title', max_length=256, null=True, verbose_name='title')),
                ('description', models.TextField(blank=True, help_text='Cloud storage description', null=True, verbose_name='description')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Creation time', verbose_name='created at')),
                ('last_sync', models.DateTimeField(blank=True, help_text='Last sync finished time', null=True, verbose_name='last sync')),
                ('last_sync_count', models.PositiveIntegerField(blank=True, help_text='Count of tasks synced last time', null=True, verbose_name='last sync count')),
                ('can_delete_objects', models.BooleanField(blank=True, help_text='Deletion from storage enabled', null=True, verbose_name='can_delete_objects')),
            ],
            options={
                'abstract': False,
            },
            bases=('io_storages.azureblobstoragemixin', models.Model),
        ),
        migrations.CreateModel(
            name='AzureBlobImportStorage',
            fields=[
                ('azureblobstoragemixin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='io_storages.azureblobstoragemixin')),
                ('title', models.CharField(blank=True, help_text='Cloud storage title', max_length=256, null=True, verbose_name='title')),
                ('description', models.TextField(blank=True, help_text='Cloud storage description', null=True, verbose_name='description')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Creation time', verbose_name='created at')),
                ('last_sync', models.DateTimeField(blank=True, help_text='Last sync finished time', null=True, verbose_name='last sync')),
                ('last_sync_count', models.PositiveIntegerField(blank=True, help_text='Count of tasks synced last time', null=True, verbose_name='last sync count')),
                ('presign', models.BooleanField(default=True, help_text='Generate presigned URLs', verbose_name='presign')),
                ('presign_ttl', models.PositiveSmallIntegerField(default=1, help_text='Presigned URLs TTL (in minutes)', verbose_name='presign_ttl')),
            ],
            options={
                'abstract': False,
            },
            bases=('io_storages.azureblobstoragemixin', models.Model),
        ),
        migrations.CreateModel(
            name='GCSExportStorage',
            fields=[
                ('gcsstoragemixin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='io_storages.gcsstoragemixin')),
                ('title', models.CharField(blank=True, help_text='Cloud storage title', max_length=256, null=True, verbose_name='title')),
                ('description', models.TextField(blank=True, help_text='Cloud storage description', null=True, verbose_name='description')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Creation time', verbose_name='created at')),
                ('last_sync', models.DateTimeField(blank=True, help_text='Last sync finished time', null=True, verbose_name='last sync')),
                ('last_sync_count', models.PositiveIntegerField(blank=True, help_text='Count of tasks synced last time', null=True, verbose_name='last sync count')),
                ('can_delete_objects', models.BooleanField(blank=True, help_text='Deletion from storage enabled', null=True, verbose_name='can_delete_objects')),
            ],
            options={
                'abstract': False,
            },
            bases=('io_storages.gcsstoragemixin', models.Model),
        ),
        migrations.CreateModel(
            name='GCSImportStorage',
            fields=[
                ('gcsstoragemixin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='io_storages.gcsstoragemixin')),
                ('title', models.CharField(blank=True, help_text='Cloud storage title', max_length=256, null=True, verbose_name='title')),
                ('description', models.TextField(blank=True, help_text='Cloud storage description', null=True, verbose_name='description')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Creation time', verbose_name='created at')),
                ('last_sync', models.DateTimeField(blank=True, help_text='Last sync finished time', null=True, verbose_name='last sync')),
                ('last_sync_count', models.PositiveIntegerField(blank=True, help_text='Count of tasks synced last time', null=True, verbose_name='last sync count')),
                ('presign', models.BooleanField(default=True, help_text='Generate presigned URLs', verbose_name='presign')),
                ('presign_ttl', models.PositiveSmallIntegerField(default=1, help_text='Presigned URLs TTL (in minutes)', verbose_name='presign_ttl')),
            ],
            options={
                'abstract': False,
            },
            bases=('io_storages.gcsstoragemixin', models.Model),
        ),
        migrations.CreateModel(
            name='LocalFilesExportStorage',
            fields=[
                ('localfilesmixin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='io_storages.localfilesmixin')),
                ('title', models.CharField(blank=True, help_text='Cloud storage title', max_length=256, null=True, verbose_name='title')),
                ('description', models.TextField(blank=True, help_text='Cloud storage description', null=True, verbose_name='description')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Creation time', verbose_name='created at')),
                ('last_sync', models.DateTimeField(blank=True, help_text='Last sync finished time', null=True, verbose_name='last sync')),
                ('last_sync_count', models.PositiveIntegerField(blank=True, help_text='Count of tasks synced last time', null=True, verbose_name='last sync count')),
                ('can_delete_objects', models.BooleanField(blank=True, help_text='Deletion from storage enabled', null=True, verbose_name='can_delete_objects')),
            ],
            options={
                'abstract': False,
            },
            bases=('io_storages.localfilesmixin', models.Model),
        ),
        migrations.CreateModel(
            name='LocalFilesImportStorage',
            fields=[
                ('localfilesmixin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='io_storages.localfilesmixin')),
                ('title', models.CharField(blank=True, help_text='Cloud storage title', max_length=256, null=True, verbose_name='title')),
                ('description', models.TextField(blank=True, help_text='Cloud storage description', null=True, verbose_name='description')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Creation time', verbose_name='created at')),
                ('last_sync', models.DateTimeField(blank=True, help_text='Last sync finished time', null=True, verbose_name='last sync')),
                ('last_sync_count', models.PositiveIntegerField(blank=True, help_text='Count of tasks synced last time', null=True, verbose_name='last sync count')),
            ],
            options={
                'abstract': False,
            },
            bases=('io_storages.localfilesmixin', models.Model),
        ),
        migrations.CreateModel(
            name='RedisExportStorage',
            fields=[
                ('redisstoragemixin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='io_storages.redisstoragemixin')),
                ('title', models.CharField(blank=True, help_text='Cloud storage title', max_length=256, null=True, verbose_name='title')),
                ('description', models.TextField(blank=True, help_text='Cloud storage description', null=True, verbose_name='description')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Creation time', verbose_name='created at')),
                ('last_sync', models.DateTimeField(blank=True, help_text='Last sync finished time', null=True, verbose_name='last sync')),
                ('last_sync_count', models.PositiveIntegerField(blank=True, help_text='Count of tasks synced last time', null=True, verbose_name='last sync count')),
                ('can_delete_objects', models.BooleanField(blank=True, help_text='Deletion from storage enabled', null=True, verbose_name='can_delete_objects')),
                ('db', models.PositiveSmallIntegerField(default=2, help_text='Server Database', verbose_name='db')),
            ],
            options={
                'abstract': False,
            },
            bases=('io_storages.redisstoragemixin', models.Model),
        ),
        migrations.CreateModel(
            name='RedisImportStorage',
            fields=[
                ('redisstoragemixin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='io_storages.redisstoragemixin')),
                ('title', models.CharField(blank=True, help_text='Cloud storage title', max_length=256, null=True, verbose_name='title')),
                ('description', models.TextField(blank=True, help_text='Cloud storage description', null=True, verbose_name='description')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Creation time', verbose_name='created at')),
                ('last_sync', models.DateTimeField(blank=True, help_text='Last sync finished time', null=True, verbose_name='last sync')),
                ('last_sync_count', models.PositiveIntegerField(blank=True, help_text='Count of tasks synced last time', null=True, verbose_name='last sync count')),
                ('db', models.PositiveSmallIntegerField(default=1, help_text='Server Database', verbose_name='db')),
            ],
            options={
                'abstract': False,
            },
            bases=('io_storages.redisstoragemixin', models.Model),
        ),
        migrations.CreateModel(
            name='S3ImportStorageLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.TextField(help_text='External link key', verbose_name='key')),
                ('object_exists', models.BooleanField(default=True, help_text='Whether object under external link still exists', verbose_name='object exists')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Creation time', verbose_name='created at')),
                ('storage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='links', to='io_storages.s3importstorage')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
