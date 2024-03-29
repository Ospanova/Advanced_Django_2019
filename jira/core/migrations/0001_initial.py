# Generated by Django 2.0 on 2019-12-11 17:23

from django.db import migrations, models
import django.db.models.manager
import utils.upload
import utils.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'TODO'), (2, 'IN_PROGRESS'), (3, 'DONE'), (0, 'NEW')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('descr', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('descr', models.CharField(max_length=1000)),
                ('order', models.IntegerField()),
            ],
            managers=[
                ('tasks', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='TaskComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=1000)),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='TaskDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.FileField(null=True, upload_to=utils.upload.task_document_path, validators=[utils.validators.validate_file_size, utils.validators.validate_extension])),
            ],
        ),
    ]
