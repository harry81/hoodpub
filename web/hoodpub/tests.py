# -*- coding: utf-8 -*-
import json
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status

from .models import Read
from book.models import Book


class HoodpubTestCase(TestCase):

    fixtures = ['auth_user', 'book_book', 'hoodpub_read']

    def setUp(self):
        self.client = APIClient()
        self.client_without_csrf = APIClient()

        self.usr = User.objects.create_user(username='hoodpub',
                                            password='password',
                                            email='hoodpub@hoodpub.com')

        self.book1 = Book.objects.all()[1]
        self.book2 = Book.objects.all()[2]

    def test_facebook_action_read(self):
        # login
        post_data = {
            'username': u'hoodpub',
            'password': u'password',
        }

        res = self.client.post('/api-token-auth/', post_data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        token = json.loads(res.content)['token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        res = self.client.post('/api-hoodpub/read/',
                               {'isbn': self.book1.isbn}, format='json')

        res = self.client.post('/api-hoodpub/read/',
                               {'isbn': self.book2.isbn}, format='json')
        import ipdb; ipdb.set_trace()

        self.assertTrue(res.data['hoodpub']['success'])
        self.assertTrue(Read.objects.all().count() >= 1)

        res = self.client.post('/api-hoodpub/read/',
                               {'isbn': self.book2.isbn}, format='json')
        self.assertFalse(res.data['hoodpub']['success'])
