# -*- coding: utf-8 -*-
from django.template import RequestContext, loader
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site

from rest_framework import viewsets
from rest_framework.decorators import (list_route,
                                       detail_route, permission_classes)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from threadedcomments.models import ThreadedComment

from .serializers import UserProfileSerializer, ThreadedCommentSerializer
from .tasks import async_facebook_action_books_read

from book.serializers import BookListSerializer
from book.models import Book


def index(request):
    template = loader.get_template('hoodpub/index.html')
    current_site = request.build_absolute_uri()

    objects = None
    context = RequestContext(request, {
        'objects': objects,
        'current_site': current_site,
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
    serializer_class = BookListSerializer
    queryset = Book.objects.all()

    @permission_classes((AllowAny, ))
    def list(self, request, *args, **kwargs):
        return super(HoodpubAPIView, self).list(request, *args, **kwargs)

    @permission_classes((AllowAny, ))
    @detail_route(methods=['get'])
    def users(self, request, *args, **kwargs):
        self.queryset = self.get_queryset().filter(
            read__userprofile__sns_id=kwargs['pk']).order_by(
                '-read__created_at')

        return super(HoodpubAPIView, self).list(request, *args, **kwargs)

    @permission_classes((IsAuthenticated, ))
    @list_route(methods=['post'])
    def read(self, request, *args, **kwargs):
        user_profile = self.request.user.userprofile_set.all()[0]
        kwargs['isbn'] = request.data['isbn']
        res_hoodpub = user_profile.set_read(request, *args, **kwargs)
        async_facebook_action_books_read.delay(user_profile.sns_id,
                                               kwargs['isbn'])

        resp = {
            'hoodpub': res_hoodpub
        }
        return Response(resp)


class CommentAPIView(viewsets.ModelViewSet):
    serializer_class = ThreadedCommentSerializer
    queryset = ThreadedComment.objects.all()

    @permission_classes((AllowAny, ))
    @detail_route(methods=['get'])
    def book(self, request, *args, **kwargs):
        self.queryset = self.get_queryset().filter(
            content_type=ContentType.objects.get(app_label="book", model="book"),
            object_pk=kwargs['pk'])
        return super(CommentAPIView, self).list(request, *args, **kwargs)

    @permission_classes((AllowAny, ))
    @detail_route(methods=['get'])
    def user(self, request, *args, **kwargs):
        self.queryset = self.get_queryset().filter(
            content_type=ContentType.objects.get(app_label="book", model="book"),
            user_id=kwargs['pk'])

        return super(CommentAPIView, self).list(request, *args, **kwargs)

    @permission_classes((IsAuthenticated, ))
    @list_route(methods=['post'])
    def onesentense(self, request, *args, **kwargs):

        res = ThreadedComment.objects.create(
            content_type=ContentType.objects.get(app_label="book", model="book"),
            content_object=Book.objects.get(isbn=request.data['isbn']),
            comment=request.data['comment'],
            user=self.request.user,
            site=Site.objects.all()[0],
            )
        resp = {
            'comment': 'ok'
        }

        return Response(resp)
