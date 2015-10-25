# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hoodpub', '0006_userprofile_sns_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='facebook_access_token',
            field=models.CharField(max_length=512),
            preserve_default=True,
        ),
    ]
