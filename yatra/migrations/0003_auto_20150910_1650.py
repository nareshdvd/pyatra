# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yatra', '0002_auto_20150903_0925'),
    ]

    operations = [
        migrations.CreateModel(
            name='RenderJob',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(max_length=50, choices=[(b'hold', b'hold'), (b'sent', b'sent'), (b'started', b'started'), (b'failed', b'failed'), (b'finished', b'finished')])),
                ('status_message', models.TextField(default=None, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='RenderServer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip_address', models.CharField(max_length=60)),
                ('port', models.CharField(max_length=10)),
                ('jobs_count', models.IntegerField(default=0, null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='videosession',
            name='compressed_file',
            field=models.TextField(default=None, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='renderjob',
            name='render_server',
            field=models.ForeignKey(related_name='server_render_jobs', to='yatra.RenderServer'),
        ),
        migrations.AddField(
            model_name='renderjob',
            name='session',
            field=models.ForeignKey(related_name='session_render_jobs', to='yatra.VideoSession'),
        ),
    ]
