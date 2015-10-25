# -*- coding: utf-8 -*-
from django.test import TestCase


class HoodpubTestCase(TestCase):

    fixtures = ['book']

    def test_facebook_action_read(self):
        res = self.client.post('/api-hoodpub/read/',
                               {'isbn': u'8995843543'}, format='json')
        self.assertIn('id', res.data.text)
