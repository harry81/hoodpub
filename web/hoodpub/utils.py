# -*- coding: utf-8 -*-

import requests
from urlparse import urljoin
from django.conf import settings
from book.models import Book


def facebook_action_read(request):
    isbn = request.POST.get('isbn')
    book = Book.objects.get(isbn=isbn)

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
    import ipdb; ipdb.set_trace()
    res = requests.post(url, params=url_dict, json=data_dict)

    return res
