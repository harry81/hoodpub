# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.db.models import Q
from book.models import Book
from hoodpub.models import Read
from hoodpub.utils import delete_reads


def forwards_func(apps, schema_editor):
    try:
        total_book_before = Book.objects.count()
        total_read_before = Read.objects.count()

        books = Book.objects.filter(
            Q(title__icontains='주님의 기쁨되', isbn='') |
            Q(isbn__in=['2234673003', '1739208005', '4758012490', '0076592529', '0076592529',
                        '1739208005', '0076592529', '8994221328', '8993769842', '8992437536',
                        '8955661266', '8960673552', '8960673552', '8955661266', '8993952426',
                        '8992037724', '8960673560', '1419705849', '1419705849', '8964167198',
                        '8992037724', '8960673560', '8964167198', '8952765141', '8992037724'])
        )

        for book in books:
            delete_reads(book)

    except:
        print 'no book'
        pass

    total_book_after = Book.objects.count()
    total_read_after = Read.objects.count()

    print "\nBEFORE book [%d], read [%d]" % (total_book_before, total_read_before )
    print "AFTER  book [%d], read [%d]" % (total_book_after, total_read_after )


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('hoodpub', '0016_auto_20151108_1112'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
