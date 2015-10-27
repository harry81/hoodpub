# -*- coding: utf-8 -*-
import json

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Book
from .utils import search_via_book_api


class BookTestCase(TestCase):

    fixtures = ['auth', 'book', 'reads']

    def setUp(self):
        self.client = APIClient()
        self.client_without_csrf = APIClient()

    def test_api_book_load(self):
        self.skipTest(True)
        res = self.client.get('/api-book/load/',
                              {'title': u'삼국지'}, format='json')
        res = json.loads(res.content)
        self.assertTrue(Book.objects.all().count() > 10)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_search_via_book_api(self):
        self.skipTest(True)
        res = search_via_book_api(title=u'한국사')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_api_list(self):
        res = self.client.get('/api-book/',
                              {'search': u'수학'}, format='json')
        data = json.loads(res.content)

        self.assertIn('total_read',
                      data['results'][0].keys())
        self.assertIn('sns_id',
                      data['results'][0]['reads'][0]['user'][0])
        self.assertTrue(Book.objects.all().count() > 10)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
