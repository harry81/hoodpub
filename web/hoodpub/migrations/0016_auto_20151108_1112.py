# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('hoodpub', '0015_auto_20151025_2116'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='read',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AlterField(
            model_name='read',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime.now, db_index=True, blank=True),
            preserve_default=True,
        ),
    ]
