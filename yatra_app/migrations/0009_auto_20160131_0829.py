# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yatra_app', '0008_auto_20160126_1715'),
    ]

    operations = [
        migrations.AddField(
            model_name='videosession',
            name='rendering_finished',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='videosession',
            name='rendering_percentage',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='videosession',
            name='rendering_started',
            field=models.BooleanField(default=False),
        ),
    ]
