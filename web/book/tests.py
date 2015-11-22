# -*- coding: utf-8 -*-
import json
from mock import patch
from requests import exceptions

from django.core.cache import cache

from django.test import TestCase
from django.http import HttpResponse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
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

        self.book1 = Book.objects.get(isbn='0141344989')
        self.book2 = Book.objects.all()[2]

    @patch('requests.get')
    def test_api_book_load(self, mock_requests):
        book_response = open('book/fixtures/book_response_from_daum.mock',
                             'rt').read()
        mock_requests.return_value = HttpResponse(book_response)
        mock_requests.status_code = 200

        res = self.client.get('/api-book/load/',
                              {'title': self.book1.title}, format='json')

        self.assertTrue(Book.objects.all().count() > 10)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    @patch('requests.get')
    def test_search_via_book_api(self, mock_requests):
        book_response = open('book/fixtures/book_response_from_daum.mock',
                             'rt').read()
        mock_requests.return_value = HttpResponse(book_response)
        mock_requests.status_code = 200

        res = search_via_book_api(title=self.book1.title)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    @patch('requests.get')
    def test_search_via_book_api_with_none_isbn(self, mock_requests):
        book_response = open('book/fixtures/book_response_'
                             'from_daum_with_none_isbn.mock',
                             'rt').read()
        mock_requests.return_value = HttpResponse(book_response)
        mock_requests.status_code = 200

        book_cnt_before = Book.objects.count()

        json_output = json.loads(book_response)
        isbn_cnt = len(json_output['channel']['item'])

        res = search_via_book_api(title=self.book1.title)
        book_cnt_after = Book.objects.count()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(book_cnt_after, book_cnt_before + isbn_cnt - 1)

    def test_api_list(self):
        res = self.client.get('/api-book/',
                              {'search': self.book1.title}, format='json')
        data = json.loads(res.content)

        self.assertIn('total_read',
                      data['results'][0].keys())
        self.assertTrue(Book.objects.all().count() > 4)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_sns_id_exist(self):
        self.client.post('/api-hoodpub/read/',
                         {'isbn': self.book1.isbn}, format='json')

        self.assertEqual(self.book1.read_set.all()[0]
                         .userprofile_set.all()[0].sns_id,
                         u'213232')

    @patch('requests.get')
    def test_rename_cover_url_into_https(self, mock_requests):
        self.assertIn('http', self.book1.cover_s_url)
        self.assertNotIn('https', self.book1.cover_s_url)
        mock_requests.status_code = 200
        self.book1.rename_cover_url()
        self.assertIn('https', self.book1.cover_s_url)

    @patch('requests.get')
    def test_rename_cover_url_into_https_with_empty_url(self, mock_requests):
        self.book1.cover_s_url = ''
        self.book1.save()
        e = exceptions.MissingSchema(
            "Invalid URL '': No schema supplied. Perhaps you meant http://?")
        mock_requests.side_effect = e
        res = self.book1.rename_cover_url()
        self.assertFalse(res)

    def test_search_keyword_cache(self):
        res1 = self.client.get('/api-book/',
                               {'search': u'검색어'}, format='json')

        search_keyword = cache.get('search_keyword')
        self.assertTrue(search_keyword[0], u'검색어')

        res2 = self.client.get('/api-book/',
                               {'search': u'검색어'}, format='json')
        data1 = json.loads(res1.content)
        data2 = json.loads(res2.content)

        self.assertTrue(data1, data2)

    @patch('requests.get')
    def test_get_description_from_url(self, mock_requests):
        book_response = open('book/fixtures/'
                             'book_detail_from_daum.mock',
                             'rt').read()
        mock_requests.return_value = HttpResponse(book_response)
        mock_requests.status_code = 200
        descs = self.book1._get_description_from_url()

        self.assertIn('때문입니다.', descs[0].encode('utf-8'))
        self.assertIn('반증이기도', descs[1].encode('utf-8'))


    @patch('requests.get')
    def test_get_description(self, mock_requests):
        book_response = open('book/fixtures/'
                             'book_detail_from_daum.mock',
                             'rt').read()
        mock_requests.return_value = HttpResponse(book_response)
        mock_requests.status_code = 200
        self.assertIn('기발한', self.book1.description.encode('utf-8'))
        descs = self.book1.get_description()
        self.assertNotIn('기발한', self.book1.description.encode('utf-8'))
        self.assertIn('무조건', self.book1.description.encode('utf-8'))
        
        
