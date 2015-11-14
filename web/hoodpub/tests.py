# -*- coding: utf-8 -*-
import json
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
