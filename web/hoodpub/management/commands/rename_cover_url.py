from django.core.management.base import BaseCommand
from book.models import Book


class Command(BaseCommand):
    help = "My shiny new management command."

    def handle(self, *args, **options):
        for book in Book.objects.all()[0:11]:
            resp = book.rename_cover_url()
            print "[%r] %s\n%s\n%s" % (resp, book.title, book.cover_s_url, book.cover_l_url)
