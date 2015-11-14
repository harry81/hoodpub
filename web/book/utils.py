# -*- coding: utf-8 -*-

import requests
import json
import HTMLParser
from datetime import datetime

from django.conf import settings
from django.utils.html import strip_tags
from .models import Book

parser = HTMLParser.HTMLParser()


def save_books(items):
    for item in items:
        item['isbn'] = _trim_text(item['isbn'])
        if len(item['isbn']) == 0:
            continue

        item['pub_date'] = datetime.strptime(item['pub_date'], '%Y%m%d')
        item['title'] = _trim_text(item['title'])
        item['description'] = _trim_text(item['description'])
        item['pub_nm'] = _trim_text(item['pub_nm'])
        item['author'] = _trim_text(item['author'])
        item['author_t'] = _trim_text(item['author_t'])
        item['isbn13'] = _trim_text(item['isbn13'])
        book, created = Book.objects.update_or_create(
            isbn=item['isbn'], defaults=item)
        if created:
            book.rename_cover_url()

    return True


def _trim_text(data):
    return strip_tags(parser.unescape(data))


def search_via_book_api(url='https://apis.daum.net/search/book',
                        output='json',
                        pageno=1,
                        title=None):

    if title is None:
        return None

    if pageno > settings.MAX_PAGE_NUM_OF_DAUM:
        return None

    params = {
        'apikey': settings.DAUM_APIKEY,
        'q': title,
        'output': u'json',
        'result': 20,
        'pageno': pageno,
        'sort': 'accu'
    }
    res = requests.get(url, params=params)

    if res.status_code == 429:
        return {'reponse': 'Too many request',
                'msg': res.content
                }
    json_output = json.loads(res.content)

    save_books(json_output['channel']['item'])

    if pageno * params['result'] < int(json_output['channel']['totalCount']):
        search_via_book_api(url, output, pageno + 1, title=title)

    return res
