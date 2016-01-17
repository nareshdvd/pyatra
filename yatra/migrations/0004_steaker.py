# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yatra', '0003_auto_20150910_1650'),
    ]

    operations = [
        migrations.CreateModel(
            name='Steaker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'steakers')),
            ],
        ),
    ]
