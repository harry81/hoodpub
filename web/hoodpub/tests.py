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
        self.profile = self.usr.userprofile_set.all()[0]
        self.profile.sns_id = '213232'
        self.profile.save(update_fields=['sns_id'])

        self.book1 = Book.objects.all()[1]
        self.book2 = Book.objects.all()[2]

        # login
        post_data = {
            'username': u'hoodpub',
            'password': u'password',
        }

        res = self.client.post('/api-token-auth/', post_data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        token = json.loads(res.content)['token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_facebook_action_read(self):

        res = self.client.post('/api-hoodpub/read/',
                               {'isbn': self.book1.isbn}, format='json')

        res = self.client.post('/api-hoodpub/read/',
                               {'isbn': self.book2.isbn}, format='json')

        self.assertTrue(res.data['hoodpub']['success'])
        self.assertTrue(Read.objects.all().count() >= 1)

        res = self.client.post('/api-hoodpub/read/',
                               {'isbn': self.book2.isbn}, format='json')
        self.assertFalse(res.data['hoodpub']['success'])

    def test_is_read_by_user(self):
        res = self.client.post('/api-hoodpub/read/',
                               {'isbn': self.book1.isbn}, format='json')
        res = self.client.get('/api-book/',
                              {'title': self.book1.title}, format='json')
        data = json.loads(res.content)
        self.assertTrue(data['results'][0]['is_read'])

    def test_users(self):
        res = self.client.post('/api-hoodpub/read/',
                               {'isbn': self.book1.isbn}, format='json')

        res = self.client.get('/api-hoodpub/%s/users/' % self.profile.sns_id)
        data = json.loads(res.content)
        self.assertEqual(1, data['count'])
