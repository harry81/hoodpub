# -*- coding: utf-8 -*-
from django.test import TestCase


class HoodpubAuthTestCase(TestCase):
    fixtures = ['auth_user', 'book_book', 'hoodpub_read']

    def test_assert(self):
        self.assertTrue(True)
