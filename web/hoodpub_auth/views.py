# -*- coding: utf-8 -*-
import requests
import urlparse

from django.contrib.auth import login
from social.apps.django_app.utils import psa

from django.http import HttpResponse
from django.conf import settings
from .utils import get_access_token


@psa('social:complete')
def register_by_access_token(request, backend):
    # This view expects an access_token GET parameter, if it's needed,
    # request.backend and request.strategy will be loaded with the current
    # backend and strategy.
    if 'code' not in request.GET:
        HttpResponse("No code in request.GET")

    get_code_payload = {
        'client_id': settings.SOCIAL_AUTH_FACEBOOK_KEY,
        'client_secret': settings.SOCIAL_AUTH_FACEBOOK_SECRET,
        'redirect_uri': settings.SOCIAL_AUTH_FACEBOOK_REDIRECT,
        'code': request.GET.get('code')
        }
    url = 'https://graph.facebook.com/oauth/access_token'
    res = requests.get(url, params=get_code_payload)

    token = urlparse.parse_qs(res.content)['access_token'][0]
    user = request.backend.do_auth(token)

    if user:
        login(request, user)
        token = get_access_token(user)
        template = loader.get_template('berlinreport/gateway.html')
        context = RequestContext(request, {
            'objects': token.content,
        })
        return HttpResponse(template.render(context))

    else:
        return HttpResponse("error")
