# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hoodpub', '0012_remove_userprofile_timezone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='birthday',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='email',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='link',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='locale',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='name',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='updated_time',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='verified',
        ),
    ]
