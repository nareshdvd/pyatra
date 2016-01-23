# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yatra_app', '0006_steaker'),
    ]

    operations = [
        migrations.AddField(
            model_name='videosession',
            name='video_category',
            field=models.ForeignKey(related_name='category_video_sessions', default=2, to='yatra_app.Category'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='videosession',
            name='video_template',
            field=models.ForeignKey(related_name='template_video_sessions', to='yatra_app.VideoTemplate'),
        ),
    ]
