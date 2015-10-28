# -*- coding: utf-8 -*-
import json
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status

from .models import Read


class HoodpubTestCase(TestCase):

    fixtures = ['book']

    def setUp(self):
        self.client = APIClient()
        self.client_without_csrf = APIClient()

        usr = User.objects.create_user(username='hoodpub',
                                       password='password',
                                       email='hoodpub@hoodpub.com')
        profile = usr.userprofile_set.all()[0]


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
                               {'isbn': u'8914018261'}, format='json')

        res = self.client.post('/api-hoodpub/read/',
                               {'isbn': u'8936430440'}, format='json')

        self.assertTrue(res.data['hoodpub']['success'])
        self.assertIn('book', res.data['hoodpub'])
        self.assertTrue(Read.objects.all().count() >= 1)

        res = self.client.post('/api-hoodpub/read/',
                               {'isbn': u'8936430440'}, format='json')
        self.assertFalse(res.data['hoodpub']['success'])

