# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hoodpub', '0008_auto_20151025_1731'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='timezone',
        ),
    ]
