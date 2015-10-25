# -*- coding: utf-8 -*-

import requests
from urlparse import urljoin


def facebook_action_read(request):

    url_dict = {
        'access_token': 'CAAKaRbf67W8BAPwbVrLJ7twVaRQbxzF8BnKFBhytyUZBJX9e8gsHMYFU77O2bJWN1ZBBvZBaAu4euAewzp422cIk4jRIH7facChyBFCMV98AWlMYz3uXkxSGjZCbN5LCFhaXglRZBLNyqnfZAdPLtZCBXJE0VO0rV7svn3lPVOWPnLsacWemmjF2ICxKGA7OnEZD',
        'mothod': 'POST',
    }
    
    data_dict = {
        "object":
        {
            "books:author": "http://samples.ogp.me/344562145628374",
            "books:isbn": "0553380958",
            "fb:app_id": 732574183517551,
            "og:description": "In reality, Hiro Protagonist delivers pizza for Uncle Enzo\u2019s CosoNostra Pizza Inc., but in the Metaverse he\u2019s a warrior prince. Plunging headlong into the enigma of a new computer virus that\u2019s striking down hackers everywhere, he races along the neon-lit streets on a search-and-destroy mission for the shadowy virtual villain threatening to bring about infocalypse. Snow Crash is a mind-altering romp through a future America so bizarre, so outrageous\u2026you\u2019ll recognize it immediately.",
            "og:image": "http://en.wikipedia.org/wiki/File:Snowcrash.jpg",
            "og:type": "books.book",
            "og:title": "Snow Crash",
            "og:url": "https://www.facebook.com/pages/Anne-Frank-The-Young-Writer-Who-Told-the-World-Her-Story/477596482277558?rf=316285781810761"
        }
    }

    url = 'https://graph.facebook.com/'
    action = 'me/objects/books.book'
    url = urljoin(url, action)
    res = requests.post(url, params=url_dict, json=data_dict)

    return res
