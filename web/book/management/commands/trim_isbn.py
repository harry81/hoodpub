from django.core.management.base import BaseCommand
from django.utils.html import strip_tags
import HTMLParser

from book.models import Book


class Command(BaseCommand):
    help = "My shiny new management command."
    parser = HTMLParser.HTMLParser()

    def handle(self, *args, **options):
        for book in Book.objects.all():
            if len(book.isbn) > 11:
                cnt = book.read_set.all().count()
                if cnt > 1:
                    old_book = book
                    isbn = strip_tags(self.parser.unescape(book.isbn))
                    try:
                        new_book = Book.objects.get(isbn=isbn)
                    except Book.DoesNotExist:
                        continue

                    for read in old_book.read_set.all():
                        self.stdout.write("OLD %14s - %14s\n" %
                                          (book.isbn, read)
                                          , ending='')

                    for read in new_book.read_set.all():
                        self.stdout.write("NEW %14s - %14s %d\n" % (book.isbn, read, read.id)
                                          ,ending='')


                    for read in old_book.read_set.all():
                        read.book = new_book
                        read.save()

                    for read in old_book.read_set.all():
                        self.stdout.write("OLD %14s - %14s %d\n" % (book.isbn, read, read.id)
                                          ,ending='')

                    for read in new_book.read_set.all():
                        self.stdout.write("NEW %14s - %14s %d\n" % (book.isbn, read, read.id)
                                          ,ending='')
