# -*- coding: utf-8 -*-
from django.template import RequestContext, loader
from django.http import HttpResponse


def index(request):
    template = loader.get_template('hoodpub/index.html')
    objects = None
    context = RequestContext(request, {
        'objects': objects,
    })
    return HttpResponse(template.render(context))
