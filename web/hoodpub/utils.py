# -*- coding: utf-8 -*-
import requests
import json
from urlparse import urljoin
from django.utils.html import strip_tags
import HTMLParser
from templated_email import send_templated_mail

from book.models import Book
from hoodpub.models import User


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


def facebook_set_profile(request, *args, **kwargs):

    access_token = kwargs['token']
    userprofile = request.user.userprofile_set.all()[0]

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


def facebook_action_read(sns_id, isbn):
    user = User.objects.get(userprofile__sns_id=sns_id)
    book = Book.objects.get(isbn=isbn)

    url_dict = {
        'access_token': '%s' %
        user.userprofile_set.all()[0].facebook_access_token,
        'mothod': 'POST',
        'book': 'https://hoodpub.com/book/%s/' % isbn
    }

    url = 'https://graph.facebook.com/'
    action = 'me/hoodpub:read'
    url = urljoin(url, action)
    res = requests.post(url, params=url_dict)
    _send_email_after_read(user, book)

    return res
