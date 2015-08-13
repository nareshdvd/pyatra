# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoSession',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('session_id', models.CharField(max_length=255)),
                ('timestamp', models.CharField(default=b'', max_length=255, blank=True)),
                ('video_generated', models.BooleanField(default=False)),
                ('video', models.FileField(null=True, upload_to=b'final_videos', blank=True)),
                ('user', models.ForeignKey(related_name='video_sessions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='VideoTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=500)),
                ('demo_file', models.FileField(upload_to=b'template_demo_videos')),
                ('project_compressed_file', models.FileField(upload_to=b'zipped_projects')),
                ('item_positions', models.TextField(default=b'', null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='VideoTemplateCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=500)),
                ('description', models.TextField(default=b'', null=True, blank=True)),
                ('cover_image', models.ImageField(default=None, null=True, upload_to=b'category_images', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='YatraContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attachment', models.FileField(upload_to=b'uploads')),
                ('content_type', models.CharField(max_length=10, choices=[(b'IMAGE', b'IMAGE'), (b'AUDIO', b'AUDIO'), (b'VIDEO', b'VIDEO')])),
                ('content_order', models.IntegerField(default=0, null=True, blank=True)),
                ('video_session', models.ForeignKey(related_name='contents', to='yatra.VideoSession')),
            ],
            options={
                'verbose_name': 'Yatra Content',
                'verbose_name_plural': 'Yarta Contents',
            },
        ),
        migrations.AddField(
            model_name='videotemplate',
            name='categories',
            field=models.ManyToManyField(related_name='category_templates', to='yatra.VideoTemplateCategory'),
        ),
        migrations.AddField(
            model_name='videosession',
            name='video_template',
            field=models.ForeignKey(related_name='template_video_sessions', to='yatra.VideoTemplate'),
        ),
    ]
