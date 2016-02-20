# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('render_app', '0002_auto_20160220_0907'),
    ]

    operations = [
        migrations.AddField(
            model_name='renderprocess',
            name='failed_count',
            field=models.IntegerField(default=0),
        ),
    ]
