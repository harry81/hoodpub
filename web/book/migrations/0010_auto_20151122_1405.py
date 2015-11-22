# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0009_auto_20151122_1359'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='introduction',
            unique_together=set([('book', 'publisher', 'cnt')]),
        ),
    ]
