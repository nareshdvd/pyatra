# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import yatra_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('yatra_app', '0009_auto_20160131_0829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sessionitem',
            name='item_file',
            field=models.FileField(max_length=10000, null=True, upload_to=yatra_app.models.session_item_relative_upload_path, blank=True),
        ),
    ]
