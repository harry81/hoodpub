from django.core.management.base import BaseCommand
import HTMLParser

from book.models import Book
from hoodpub.models import Read
from hoodpub.utils import move_read_new_book


class Command(BaseCommand):
    help = "My shiny new management command."
    parser = HTMLParser.HTMLParser()

    def handle(self, *args, **options):
        book_long_isbn_before = Book.objects.filter(
            isbn__iregex=r'^.{11,}$').count()

        total_book_before = Book.objects.count()
        total_read_bofore = Read.objects.count()
        cnt_created = 0

        for old_book in Book.objects.filter(
                isbn__iregex=r'^.{11,}$'):
            new_book, created = move_read_new_book(old_book)

            if created:
                cnt_created = cnt_created + 1
                self.stdout.write("new book %s\n" % (
                    new_book), ending='')

        book_long_isbn_after = Book.objects.filter(
            isbn__iregex=r'^.{11,}$').count()
        total_book_after = Book.objects.count()
        total_read_after = Read.objects.count()

        self.stdout.write("BOFORE total books [%d], total reads [%d], "
                          "long_isbn [%d]\n" %
                          (total_book_before, total_read_bofore,
                           book_long_isbn_before), ending='')
        self.stdout.write("AFTER  total books [%d], total reads [%d], "
                          "long_isbn [%d], created [%d]\n"
                          % (total_book_after, total_read_after,
                             book_long_isbn_after, cnt_created), ending='')
