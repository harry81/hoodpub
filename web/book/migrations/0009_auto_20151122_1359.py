# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0008_introduction_cnt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='introduction',
            name='publisher',
            field=models.CharField(max_length=3, choices=[(b'KY', '\uad50\ubcf4'), (b'YE', 'YES24'), (b'IN', '\uc778\ud130\ud30c\ud06c'), (b'BA', '\ubc18\ub514\uc5d4\ub8e8\ub2c8\uc2a4')]),
            preserve_default=True,
        ),
    ]
