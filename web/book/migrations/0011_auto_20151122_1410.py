# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0010_auto_20151122_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='introduction',
            name='book',
            field=models.ForeignKey(to='book.Book'),
            preserve_default=True,
        ),
    ]
