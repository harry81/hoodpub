# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.CharField(max_length=168)),
                ('sale_yn', models.CharField(max_length=16)),
                ('barcode', models.CharField(max_length=168)),
                ('isbn', models.CharField(max_length=168)),
                ('isbn13', models.CharField(max_length=168)),
                ('cover_s_url', models.CharField(max_length=512)),
                ('author', models.CharField(max_length=168)),
                ('author_t', models.CharField(max_length=168)),
                ('sale_price', models.CharField(max_length=168)),
                ('title', models.CharField(max_length=168)),
                ('translator', models.CharField(max_length=168)),
                ('link', models.CharField(max_length=168)),
                ('etc_author', models.CharField(max_length=128)),
                ('pub_nm', models.CharField(max_length=128)),
                ('list_price', models.CharField(max_length=168)),
                ('ebook_barcode', models.CharField(max_length=168)),
                ('cover_l_url', models.CharField(max_length=512)),
                ('pub_date', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('status_des', models.CharField(max_length=168)),
                ('description', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
