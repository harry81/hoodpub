# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hoodpub', '0002_userprofile_facebook_access_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='facebook_access_token',
            field=models.CharField(max_length=256),
            preserve_default=True,
        ),
    ]
