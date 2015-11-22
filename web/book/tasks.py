# -*- coding: utf-8 -*-
from __future__ import absolute_import

import time
from celery import shared_task
from .utils import search_via_book_api


@shared_task
def async_search_via_book_api(title):
    time.sleep(5)
    return search_via_book_api(title=title)
