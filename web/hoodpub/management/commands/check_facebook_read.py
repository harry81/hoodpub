# -*- coding: utf-8 -*-
import requests
import json
from urlparse import urljoin
from constance import config
from django.core.management.base import BaseCommand
from hoodpub.utils import facebook_action_books_read
from social.apps.django_app.default.models import UserSocialAuth


class Command(BaseCommand):
    help = "Command to see if the read action works"

    def handle(self, *args, **options):
        if config.CONF_OG_TYPE == 0:
            self.hoodpub_books_read()
        elif config.CONF_OG_TYPE == 1:
            self.facebook_books_read()

    def facebook_books_read(self):
        res = facebook_action_books_read('100003956532232',
                                         '8992647913')
        data = json.loads(res.content)

        assert 'id' in data, 'Books:Read object is not created.'
        print "New hoodpub:read was created. [%s]" % (data['id'])

    def hoodpub_books_read(self):
        # get read id
        user = UserSocialAuth.objects.get(user__username=u'HarryAdaum')
        print "Getting reads of %s" % user.user.username

        url_dict = {
            'access_token': user.access_token,
        }

        url = 'https://graph.facebook.com'
        action = 'me/hoodpub:read'
        url = urljoin(url, action)
        res = requests.get(url, params=url_dict)
        data = json.loads(res.content)

        sns_id = data['data'][0]['from']['id']
        obj_id = data['data'][0]['id']
        book_url = data['data'][0]['data']['book']['url']
        print "A read is found \n[%s]" % data['data'][0]

        # delete book
        print "Deleting the read %s - %s[%s]" % (
            obj_id, book_url,
            data['data'][0]['data']['book']['title'])

        url_dict = {
            'access_token': user.access_token,
            'method': 'DELETE'
        }

        url = 'https://graph.facebook.com'
        action = obj_id
        url = urljoin(url, action)
        res = requests.get(url, params=url_dict)
        assert res.content == 'true', 'Read object is not deleted.'

        # create book
        facebook_action_books_read(sns_id,
                                   '8992647913',
                                   action='me/hoodpub:read')
        data = json.loads(res.content)

        assert 'id' in data, 'Read object is not created.'
        print "New read was created. [%s] <- %s" % (data['id'], obj_id)
