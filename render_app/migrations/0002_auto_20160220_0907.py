# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('render_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='renderprocess',
            name='process_state',
            field=models.CharField(default=b'', max_length=100, choices=[(b'', b''), (b'queued', b'queued'), (b'started', b'started'), (b'finished', b'finished'), (b'failed', b'failed')]),
        ),
        migrations.AlterField(
            model_name='renderprocess',
            name='render_server',
            field=models.ForeignKey(related_name='processes', to='render_app.RenderServer'),
        ),
    ]
