# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('yatra_app', '0002_auto_20151219_1453'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoSession',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('session_id', models.CharField(max_length=255)),
                ('project_dir', models.CharField(default='', max_length=2000, null=True, blank=True)),
                ('final_video', models.CharField(default='', max_length=2000, null=True, blank=True)),
                ('user', models.ForeignKey(related_name='video_sessions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='videotemplate',
            name='compressed_file',
            field=models.FileField(default=None, upload_to='compressed_projects'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='videotemplate',
            name='demo_file',
            field=models.FileField(default='', upload_to='demo_files'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='videosession',
            name='video_template',
            field=models.ForeignKey(related_name='video_session', to='yatra_app.VideoTemplate'),
        ),
    ]
