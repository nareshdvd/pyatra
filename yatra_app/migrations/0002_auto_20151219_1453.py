# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yatra_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='videotemplate',
            managers=[
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='cover_image',
            field=models.ImageField(default='no_image.jpg', upload_to='category_covers'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='videotemplate',
            name='cover_image',
            field=models.ImageField(default='no_image.jpg', upload_to='video_template_covers'),
            preserve_default=False,
        ),
    ]
