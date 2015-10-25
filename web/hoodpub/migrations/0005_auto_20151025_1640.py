# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('hoodpub', '0004_auto_20151025_1251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='read',
            name='book',
            field=models.ForeignKey(to='book.Book'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='read',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
