# -*- coding: utf-8 -*-
import requests
import urlparse
from django.contrib.auth import login
from django.template import RequestContext, loader
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.models import User

from social.apps.django_app.utils import psa
from social.apps.django_app.default.models import Association, Code, Nonce, UserSocialAuth
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
        profile = user.userprofile_set.all()[0]
        profile.set_facebook_profile(request, token=token)

        token = get_access_token(user)
        template = loader.get_template('hoodpub_auth/gateway.html')
        context = RequestContext(request, {
            'objects': token.content,
        })
        if User.objects.filter(email=user.email).count() > 1:
            social = UserSocialAuth.objects.get(uid=profile.sns_id)
            social.user = User.objects.filter(email=user.email)[0]
            social.save()

        return HttpResponse(template.render(context))

    else:
        return HttpResponse("error")


def auth_facebook(request):
    url_dict = {
        'client_id': settings.SOCIAL_AUTH_FACEBOOK_KEY,
        'redirect_uri': settings.SOCIAL_AUTH_FACEBOOK_REDIRECT,
        'scope': ','.join(settings.SOCIAL_AUTH_FACEBOOK_SCOPE),
    }
    url = 'https://www.facebook.com/dialog/oauth?client_id={client_id}&\
           redirect_uri={redirect_uri}&scope={scope}'.format(**url_dict)
    return redirect(url)
