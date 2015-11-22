# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0011_auto_20151122_1410'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='introduction',
            options={'ordering': ('-book',)},
        ),
        migrations.AlterField(
            model_name='book',
            name='pub_nm',
            field=models.CharField(max_length=128, db_index=True),
            preserve_default=True,
        ),
    ]
