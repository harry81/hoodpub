# -*- coding: utf-8 -*-
from django.test import TestCase


class HoodpubTestCase(TestCase):

    def test_facebook_action_read(self):
        res = self.client.post('/api-hoodpub/read/',
                               {'search': u'삼국지'}, format='json')
        self.assertIn('id', res.data.text)
