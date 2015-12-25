# -*- coding: utf-8 -*-
import requests
import time
import json
from requests import exceptions
from urlparse import urljoin
from django.utils.html import strip_tags
import HTMLParser
from templated_email import send_templated_mail
from constance import config

from book.models import Book
from social.apps.django_app.default.models import UserSocialAuth


class FacebookException(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)


def _send_email_after_read(user, book):
    send_templated_mail(
        template_name='read_action_happen',
        from_email='hoodpub@hoodpub.com',
        recipient_list=['chharry@gmail.com'],
        context={
            'userprofile': user.userprofile_set.all()[0],
            'book': book
        },
    )


def delete_reads(book):
    for read in book.read_set.all():
        read.delete()
        print '%s deleted' % book


def move_read_new_book(old_book):
    parser = HTMLParser.HTMLParser()

    isbn = strip_tags(parser.unescape(old_book.isbn))

    new_book_dict = old_book.__dict__.copy()
    for key in ['_state', 'isbn']:
        if key in new_book_dict:
            new_book_dict.pop(key)

    new_book, created = Book.objects.get_or_create(
        isbn=isbn, defaults=new_book_dict)

    if old_book.read_set.all().count() > 0:
        for read in old_book.read_set.all():
            read.book = new_book
            read.save()

    if created or Book.objects.filter(isbn__contains=isbn).count > 2:
        old_book.delete()
    return new_book, created


def facebook_set_profile(userprofile, *args, **kwargs):

    access_token = kwargs['token']

    url_dict = {
        'access_token': access_token,
    }
    url = 'https://graph.facebook.com'
    action = 'me'
    url = urljoin(url, action)
    res = requests.get(url, params=url_dict)
    data = json.loads(res.content)

    fb_fields = ['email', 'gender', 'locale', 'sns_id',
                 'facebook_access_token',
                 'name', 'last_name', 'first_name']

    userprofile.facebook_access_token = access_token
    userprofile.gender = data['gender']
    userprofile.locale = data['locale']
    userprofile.sns_id = data['id']
    userprofile.first_name = data['first_name']
    userprofile.last_name = data['last_name']
    userprofile.name = data['name']

    if 'email' in data:
        userprofile.email = data['email']
    else:
        fb_fields.pop(fb_fields.index('email'))

    userprofile.save(
        update_fields=fb_fields)


def facebook_action_books_read(sns_id, isbn):

    action = 'me/hoodpub:read' if config.CONF_OG_TYPE == 0 else 'me/books.reads'

    user = UserSocialAuth.objects.get(uid=sns_id)
    book = Book.objects.get(isbn=isbn)
    url_dict = {
        'access_token': '%s' % user.access_token,
        'mothod': 'POST',
        'book': 'https://hoodpub.com/book/%s/' % isbn,
        'progress:timestamp': int(time.time()),
        'progress:percent_complete': 100,
        'fb:explicitly_shared': 'true'
    }

    url = 'https://graph.facebook.com/'

    url = urljoin(url, action)

    try:
        res = requests.post(url, params=url_dict)
        res.raise_for_status()
    except exceptions.HTTPError, err:
        err.message = "%s - %s" % (err.message, res.content)
        raise err

    _send_email_after_read(user.user, book)

    return res
