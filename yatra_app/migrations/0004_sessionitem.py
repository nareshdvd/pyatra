# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import yatra_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('yatra_app', '0003_auto_20151219_1706'),
    ]

    operations = [
        migrations.CreateModel(
            name='SessionItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item_number', models.IntegerField()),
                ('item_type', models.CharField(max_length=100, choices=[('image', 'image'), ('video', 'video')])),
                ('item_file', models.FileField(null=True, upload_to=yatra_app.models.session_item_relative_upload_path, blank=True)),
                ('video_session', models.ForeignKey(related_name='session_items', to='yatra_app.VideoSession')),
            ],
        ),
    ]
