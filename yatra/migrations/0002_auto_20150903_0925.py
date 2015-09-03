# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yatra', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='template',
            name='variation_id',
            field=models.CharField(default=None, max_length=100, null=True, blank=True),
        ),
    ]
