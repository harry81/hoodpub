# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('hoodpub', '0005_auto_20151025_1640'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='sns_id',
            field=models.CharField(default=datetime.datetime(2015, 10, 25, 16, 45, 18, 25119, tzinfo=utc), max_length=256),
            preserve_default=False,
        ),
    ]
