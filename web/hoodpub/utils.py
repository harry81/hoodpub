# -*- coding: utf-8 -*-
import requests
import json
from urlparse import urljoin
from django.conf import settings
from django.utils.html import strip_tags
import HTMLParser

from book.models import Book


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


def facebook_action_read(request):
    isbn = request.data['isbn']

    try:
        book = Book.objects.get(isbn=isbn)
    except Book.DoesNotExist:
        return None

    url_dict = {
        'access_token': 'CAAKaRbf67W8BAPwbVrLJ7twVaRQbxzF8BnKFBhytyUZBJX9e8gsHM\
        YFU77O2bJWN1ZBBvZBaAu4euAewzp422cIk4jRIH7facChyBFCMV98AWlMYz3uXkxSGjZCb\
        N5LCFhaXglRZBLNyqnfZAdPLtZCBXJE0VO0rV7svn3lPVOWPnLsacWemmjF2ICxKGA7\
        OnEZD',
        'mothod': 'POST',
    }

    data_dict = {
        "object":
        {
            "books:author": "http://samples.ogp.me/344562145628374",
            "books:isbn": book.isbn,
            "fb:app_id": settings.SOCIAL_AUTH_FACEBOOK_KEY,
            "og:description": book.description,
            "og:image": book.cover_s_url,
            "og:type": "books.book",
            "og:title": "Snow Crash",
            "og:url": "http://localhost:8000/#/book_detail?id=8997969145",
        }
    }

    url = 'https://graph.facebook.com/'
    action = 'me/objects/books.book'
    url = urljoin(url, action)
    res = requests.post(url, params=url_dict, json=data_dict)

    return res
