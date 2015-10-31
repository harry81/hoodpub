# -*- coding: utf-8 -*-
import requests
import json
from urlparse import urljoin
from django.conf import settings
from book.models import Book


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

    userprofile.facebook_access_token = access_token
    userprofile.email = data['email']
    userprofile.gender = data['gender']
    userprofile.locale = data['locale']
    userprofile.sns_id = data['id']
    userprofile.first_name = data['first_name']
    userprofile.last_name = data['last_name']
    userprofile.name = data['name']

    userprofile.save(
        update_fields=['email', 'gender', 'locale', 'sns_id',
                       'facebook_access_token',
                       'name', 'last_name', 'first_name'])


def facebook_action_read(request):
    isbn = request.data['isbn']

    try:
        book = Book.objects.get(isbn=isbn)
    except Book.DoesNotExist:
        return None

    url_dict = {
        'access_token': 'CAAKaRbf67W8BAPwbVrLJ7twVaRQbxzF8BnKFBhytyUZBJX9e8gsHMYFU77O2bJWN1ZBBvZBaAu4euAewzp422cIk4jRIH7facChyBFCMV98AWlMYz3uXkxSGjZCbN5LCFhaXglRZBLNyqnfZAdPLtZCBXJE0VO0rV7svn3lPVOWPnLsacWemmjF2ICxKGA7OnEZD',
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
