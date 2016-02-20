# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yatra_app', '0010_auto_20160210_0501'),
    ]

    operations = [
        migrations.AddField(
            model_name='videosession',
            name='rendering_failed',
            field=models.NullBooleanField(default=None),
        ),
    ]
