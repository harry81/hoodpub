# -*- coding: utf-8 -*-
from django.template import RequestContext, loader
from django.http import HttpResponse
from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import UserProfileSerializer


def index(request):
    template = loader.get_template('hoodpub/index.html')
    objects = None
    context = RequestContext(request, {
        'objects': objects,
    })
    return HttpResponse(template.render(context))


class UserProfileAPIView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer

    def list(self, request):
        user = self.request.user.userprofile_set.all()[0]
        serializer = self.get_serializer(user, many=False)
        return Response(serializer.data)
