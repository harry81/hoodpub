# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('hoodpub', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='facebook_access_token',
            field=models.CharField(default=datetime.datetime(2015, 10, 24, 13, 45, 52, 675002, tzinfo=utc), max_length=128),
            preserve_default=False,
        ),
    ]
