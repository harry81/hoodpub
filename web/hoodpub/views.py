# -*- coding: utf-8 -*-
from django.template import RequestContext, loader
from django.http import HttpResponse
from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.decorators import list_route, detail_route, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .serializers import UserProfileSerializer
from .utils import facebook_action_read

from book.serializers import BookSerializer
from book.models import Book


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


class HoodpubAPIView(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.all()

    @permission_classes((AllowAny, ))
    def list(self, request, *args, **kwargs):
        return super(HoodpubAPIView, self).list(request, *args, **kwargs)

    @permission_classes((AllowAny, ))
    @detail_route(methods=['get'])
    def users(self, request, *args, **kwargs):
        self.queryset = self.get_queryset().filter(
            read__userprofile__sns_id=kwargs['pk']).order_by('-read__created_at')

        return super(HoodpubAPIView, self).list(request, *args, **kwargs)

    @permission_classes((IsAuthenticated, ))
    @list_route(methods=['post'])
    def read(self, request, *args, **kwargs):
        user_profile = self.request.user.userprofile_set.all()[0]
        kwargs['isbn'] = request.data['isbn']
        res_hoodpub = user_profile.set_read(request, *args, **kwargs)
        res_facebook = facebook_action_read(request)
        resp = {
            'hoodpub': res_hoodpub,
            'facebook': res_facebook
        }
        return Response(resp)
