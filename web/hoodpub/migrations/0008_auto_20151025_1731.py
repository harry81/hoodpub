# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('hoodpub', '0007_auto_20151025_1707'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='birthday',
            field=models.DateField(default=datetime.datetime.now, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='email',
            field=models.CharField(default=datetime.datetime(2015, 10, 25, 17, 30, 22, 16011, tzinfo=utc), max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='first_name',
            field=models.CharField(default=datetime.datetime(2015, 10, 25, 17, 30, 35, 169694, tzinfo=utc), max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(default='male', max_length=8),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='last_name',
            field=models.CharField(default='name', max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='link',
            field=models.CharField(default='name', max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='locale',
            field=models.CharField(default='name', max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='name',
            field=models.CharField(default='name', max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='timezone',
            field=models.CharField(default='name', max_length=32),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='updated_time',
            field=models.DateTimeField(default=datetime.datetime.now, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='verified',
            field=models.NullBooleanField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='facebook_access_token',
            field=models.CharField(max_length=256),
            preserve_default=True,
        ),
    ]
