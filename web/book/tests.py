# -*- coding: utf-8 -*-
import json

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Book
from .utils import search_via_book_api


class BookTestCase(TestCase):

    fixtures = ['auth_user', 'book_book', 'hoodpub_read']

    def setUp(self):
        self.client = APIClient()
        self.client_without_csrf = APIClient()

        # login
        post_data = {
            'username': u'hoodpub',
            'password': u'password',
        }

        usr = User.objects.create_user(
            username=post_data['username'],
            password=post_data['password'],
            email='hoodpub@hoodpub.com')
        profile = usr.userprofile_set.all()[0]
        profile.sns_id = '213232'
        profile.save(update_fields=['sns_id'])

        res = self.client.post('/api-token-auth/', post_data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        token = json.loads(res.content)['token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        self.book1 = Book.objects.all()[1]
        self.book2 = Book.objects.all()[2]

    def test_api_book_load(self):
        self.skipTest(True)
        res = self.client.get('/api-book/load/',
                              {'title': self.book1.title}, format='json')
        res = json.loads(res.content)
        self.assertTrue(Book.objects.all().count() > 10)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_search_via_book_api(self):
        self.skipTest(True)
        res = search_via_book_api(title=self.book1.title)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_api_list(self):
        res = self.client.get('/api-book/',
                              {'search': self.book1.title}, format='json')
        data = json.loads(res.content)

        self.assertIn('total_read',
                      data['results'][0].keys())
        self.assertTrue(Book.objects.all().count() > 10)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_sns_is_exist(self):
        res = self.client.post('/api-hoodpub/read/',
                               {'isbn': self.book1.isbn}, format='json')

        res = self.client.get('/api-book/',
                              {'title': self.book1.title}, format='json')
        data = json.loads(res.content)
        self.assertIn('sns_id', str(
                      data['results'][0]['reads']))
