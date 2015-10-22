# -*- coding: utf-8 -*-

import requests
import json
from datetime import datetime
from django.conf import settings
import HTMLParser
from django.utils.html import strip_tags
from .models import Books


def save_books(items):

    for item in items:
        parser = HTMLParser.HTMLParser()

        item['pub_date'] = datetime.strptime(item['pub_date'], '%Y%m%d')
        item['title'] = strip_tags(parser.unescape(item['title']))
        item['description'] = strip_tags(parser.unescape(item['description']))
        item['pub_nm'] = strip_tags(parser.unescape(item['pub_nm']))
        item['author'] = strip_tags(parser.unescape(item['author']))
        item['author_t'] = strip_tags(parser.unescape(item['author_t']))
        Books.objects.update_or_create(isbn=item['isbn'], defaults=item)


def search_via_book_api(url='https://apis.daum.net/search/book',
                        output='json',
                        pageno=1,
                        title=None):

    if title is None:
        return None

    if pageno > 10:
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
    json_output = json.loads(res.content)

    save_books(json_output['channel']['item'])
    if pageno * params['result'] < json_output['channel']['totalCount']:
        search_via_book_api(url, output, pageno + 1, title=title)

    return res
