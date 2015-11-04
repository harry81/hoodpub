import csv
from django.core.management.base import BaseCommand
from hoodpub.models import UserProfile
from book.models import Book
from book.utils import search_via_book_api
from django.db.models import Q


class Command(BaseCommand):
    help = "My shiny new management command."

    def handle(self, *args, **options):

        with open('hoodpub/fixtures/books_read.csv', 'rb') as f:
            reader = csv.reader(f)
            read_list = list(reader)

        cnt = 0
        for read in read_list:
            obj = {}
            obj['user_id'] = read[0]
            obj['facebook_id'] = read[1]
            obj['book_id'] = read[2]
            obj['isbn13'] = read[3]
            obj['title'] = read[4]
            obj['date'] = read[5]
            print obj['user_id'], obj['facebook_id'],
            obj['isbn13'], obj['title'], obj['date']

            cnt = cnt + 1
            if obj['date'] is '':
                print 'No date'
                continue

            try:
                profile = UserProfile.objects.get(user_id=obj['user_id'])
                profile.sns_id = obj['facebook_id']
                profile.save(update_fields=['sns_id'])
            except UserProfile.DoesNotExist:
                print "No userprofile %s" % obj['user_id']
                continue

            if not Book.objects.filter(isbn13=obj['isbn13']).exists():
                search_via_book_api(title=obj['isbn13'])

            book = Book.objects.filter(
                Q(isbn13=obj['isbn13']) |
                Q(isbn=obj['isbn13']) |
                Q(title__contains=obj['title'])).order_by('-isbn')

            if book.exists():
                book = book[0]
                profile.set_read(isbn=book.isbn, created_at=obj['date'])
                print 'Success [%5d]: %s read %s on %s' % (
                    cnt, profile.user.username, book.title, obj['date'])
