# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0006_auto_20151108_1114'),
    ]

    operations = [
        migrations.CreateModel(
            name='Introduction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField()),
                ('publisher', models.CharField(max_length=1, choices=[(b'KY', '\uad50\ubd80'), (b'YE', 'YES24'), (b'IN', '\uc778\ud130\ud30c\ud06c'), (b'BA', '\ubc18\ub514\uc5d4\ub8e8\ub2c8\uc2a4')])),
                ('created_at', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('updated_at', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('book', models.ForeignKey(to='book.Book', unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
