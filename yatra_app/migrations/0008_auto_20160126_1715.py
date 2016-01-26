# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import yatra_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('yatra_app', '0007_auto_20160123_0605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videosession',
            name='final_video',
            field=models.FileField(default='', null=True, upload_to=yatra_app.models.final_video_relative_upload_path, blank=True),
        ),
    ]
