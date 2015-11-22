# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0007_introduction'),
    ]

    operations = [
        migrations.AddField(
            model_name='introduction',
            name='cnt',
            field=models.IntegerField(default=0, blank=True),
            preserve_default=True,
        ),
    ]
