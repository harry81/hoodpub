# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_auto_20151022_1739'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='books',
            name='id',
        ),
        migrations.AlterField(
            model_name='books',
            name='isbn13',
            field=models.CharField(max_length=168, serialize=False, primary_key=True),
            preserve_default=True,
        ),
    ]
