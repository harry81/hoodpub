# -*- coding: utf-8 -*-
import json
from mock import patch

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status

from .models import Read
from book.models import Book
from .utils import move_read_new_book, delete_reads


class HoodpubTestCase(TestCase):

    fixtures = ['auth_user', 'book_book', 'hoodpub_read']

    def setUp(self):
        self.client = APIClient()
        self.client_without_csrf = APIClient()

        self.usr = User.objects.create_user(username='hoodpub',
                                            password='password',
                                            email='hoodpub@hoodpub.com')
        self.profile = self.usr.userprofile_set.all()[0]
        self.profile.sns_id = '1032010'
        self.profile.facebook_access_token = 'CAADnmTNgiSMBAPWASU2FOjXocA4uj'
        'xFBkCUTVyqMMXZCaHzEPtwCS5m2LyGP3RAJsmXB9ZC0ZA2CkOZCwdll5CSRyaAIpb0NL'
        'uaWME6sRZAXBg8ZAfGHffzvEnZCusbqj2sX8NEzk4g0ArRHKwCwZCSgZA9Ca8qaD4V25'
        'XZAiHyknpIpZAYQZB6eekkD20dBqI4EUzkZD'
        self.profile.save(update_fields=['sns_id', 'facebook_access_token', ])

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

    def test_read_action(self):

        res = self.client.post('/api-hoodpub/read/',
                               {'isbn': self.book1.isbn}, format='json')

        res = self.client.post('/api-hoodpub/read/',
                               {'isbn': self.book2.isbn}, format='json')

        self.assertTrue(res.data['hoodpub']['success'])
        self.assertTrue(Read.objects.all().count() >= 1)

        res = self.client.post('/api-hoodpub/read/',
                               {'isbn': self.book2.isbn}, format='json')
        self.assertFalse(res.data['hoodpub']['success'])

    @patch('requests.post')
    def test_facebook_read_action(self, mock_requests):
        mock_requests.method.return_value = '{"id":"641729025968976"}'
        mock_requests.status_code = 200
        mock_requests.raise_for_status.return_value = 'ok'

        res = self.client.post('/api-hoodpub/read/',
                               {'isbn': self.book1.isbn}, format='json')

        json_output = json.loads(res.content)
        self.assertIn('msg', json_output['hoodpub'].keys())

        from django.core.mail import outbox
        mail = outbox.pop()
        self.assertIsNotNone(mail.body)

    def test_is_read_by_user(self):
        usp = self.usr.userprofile_set.all()[0]
        self.assertNotIn(self.book1.isbn, usp.read.values_list(
            'book_id', flat=True))
        res = self.client.post('/api-hoodpub/read/',
                               {'isbn': self.book1.isbn},
                               format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(self.book1.isbn, usp.read.values_list(
            'book_id', flat=True))

    def test_users(self):
        res = self.client.post('/api-hoodpub/read/',
                               {'isbn': self.book1.isbn}, format='json')

        res = self.client.get('/api-hoodpub/%s/users/' % self.profile.sns_id)
        data = json.loads(res.content)
        self.assertEqual(1, data['count'])

    def test_trim_isbn(self):
        # setup
        for book in Book.objects.filter(isbn__contains='gt'):
            self.profile.set_read(isbn=book.isbn)
        self.assertTrue(self.profile.read.count(), 4)

        # start
        total_books = Book.objects.count()
        total_reads = Read.objects.count()

        for old_book in Book.objects.filter(isbn__iregex=r'^.{11,}$'):
            book_cnt = old_book.read_set.count()
            new_book, _ = move_read_new_book(old_book)

            self.assertEqual(old_book.read_set.all().count(), 0)
            self.assertEqual(new_book.read_set.all().count(), book_cnt)

        self.assertTrue(Book.objects.count(), total_books)
        self.assertTrue(Read.objects.count(), total_reads)

    def test_delete_read_in_book(self):
        # setup
        for book in Book.objects.filter(isbn__contains='gt'):
            self.profile.set_read(isbn=book.isbn)
        self.assertTrue(self.profile.read.count(), 4)

        book = Book.objects.get(isbn__icontains='8972882437')
        book_read = book.read_set.count()
        total_read = Read.objects.count()

        self.assertEqual(book_read, 2)

        delete_reads(book)
        self.assertEqual(book.read_set.count(), 0)
        self.assertEqual(Read.objects.count(), total_read - book_read)
