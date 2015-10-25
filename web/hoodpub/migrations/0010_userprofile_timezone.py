# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hoodpub', '0009_remove_userprofile_timezone'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='timezone',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
