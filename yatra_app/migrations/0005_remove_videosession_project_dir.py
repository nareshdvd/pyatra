# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yatra_app', '0004_sessionitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='videosession',
            name='project_dir',
        ),
    ]
