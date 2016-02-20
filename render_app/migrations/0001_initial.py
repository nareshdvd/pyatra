# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import render_app.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RenderProcess',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('process_state', models.CharField(max_length=100, choices=[(b'', b''), (b'queued', b'queued'), (b'started', b'started'), (b'finished', b'finished'), (b'failed', b'failed')])),
                ('session_id', models.IntegerField()),
                ('zipped_project', models.FileField(upload_to=render_app.models.render_project_upload_path)),
            ],
        ),
        migrations.CreateModel(
            name='RenderServer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip_address', models.CharField(max_length=100, null=True, blank=True)),
                ('port', models.CharField(max_length=10, null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='renderprocess',
            name='render_server',
            field=models.ForeignKey(to='render_app.RenderServer'),
        ),
    ]
