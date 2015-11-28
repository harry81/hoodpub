# -*- coding: utf-8 -*-
import requests
import json
from urlparse import urljoin
from django.core.management.base import BaseCommand

from social.apps.django_app.default.models import UserSocialAuth


class Command(BaseCommand):
    help = "Command to see if the read action works"

    def handle(self, *args, **options):
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
        print "Creating new read %s[%s]" % (
            book_url, data['data'][0]['data']['book']['title'])
        url_dict = {
            'access_token': user.access_token,
            'method': 'POST',
            'book': book_url
        }

        url = 'https://graph.facebook.com'
        action = 'me/hoodpub:read'
        url = urljoin(url, action)
        res = requests.get(url, params=url_dict)
        data = json.loads(res.content)
        assert 'id' in data, 'Read object is not created.'
        print "New read was created. [%s] <- %s" % (data['id'], obj_id)
