# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('hoodpub', '0014_auto_20151025_1752'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='updated_time',
            new_name='updated_at',
        ),
        migrations.AddField(
            model_name='read',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime.now, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='read',
            field=models.ManyToManyField(to='hoodpub.Read'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='read',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='read',
            name='user',
        ),
    ]
