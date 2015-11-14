from django.core.management.base import BaseCommand
from django.utils.html import strip_tags
import HTMLParser

from book.models import Book


class Command(BaseCommand):
    help = "My shiny new management command."
    parser = HTMLParser.HTMLParser()

    def handle(self, *args, **options):
        for old_book in Book.objects.filter(
                isbn__iregex=r'^.{11,}$'):
            isbn = strip_tags(self.parser.unescape(old_book.isbn))

            new_book_dict = old_book.__dict__.copy()
            for key in ['_state', 'isbn']:
                if key in new_book_dict:
                    new_book_dict.pop(key)

            new_book, created = Book.objects.get_or_create(
                isbn=isbn, defaults=new_book_dict)
            if created:
                self.stdout.write("%s created from %s\n" % (
                    new_book, old_book), ending='')

            if old_book.read_set.all().count() > 1:
                for read in old_book.read_set.all():
                    self.stdout.write("%s will point %s from %s \n" % (
                        read, new_book, old_book), ending='')

                    read.book = new_book
                    read.save()

        for old_book in Book.objects.filter(
                isbn__iregex=r'^.{11,}$'):
            old_book.delete()
            
        
        # for book in Book.objects.all():
        #     if len(book.isbn) > 11:
        #         if book.read_set.all().count() > 1:
        #             old_book = book
        #             isbn = strip_tags(self.parser.unescape(book.isbn))
        #             try:
        #                 new_book = Book.objects.get(isbn=isbn)
        #             except Book.DoesNotExist:
        #                 continue

        #             for read in old_book.read_set.all():
        #                 self.stdout.write("OLD %14s-%14s\n" % (
        #                     book.isbn, read), ending='')

        #             for read in new_book.read_set.all():
        #                 self.stdout.write("NEW %14s - %14s %d\n" % (
        #                     book.isbn, read, read.id), ending='')

        #             for read in old_book.read_set.all():
        #                 read.book = new_book
        #                 read.save()

        #             for read in old_book.read_set.all():
        #                 self.stdout.write("OLD %14s - %14s %d\n" % (
        #                     book.isbn, read, read.id), ending='')

        #             for read in new_book.read_set.all():
        #                 self.stdout.write("NEW %14s - %14s %d\n" % (
        #                     book.isbn, read, read.id), ending='')
