# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hoodpub', '0011_auto_20151025_1742'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='timezone',
        ),
    ]
