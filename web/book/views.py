# -*- coding: utf-8 -*-
from django.template import RequestContext, loader
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import Count

from django.core.cache import cache

from rest_framework import viewsets
from rest_framework import filters
from rest_framework.decorators import list_route, permission_classes
from rest_framework.permissions import AllowAny

from .serializers import BookListSerializer
from .models import Book
from hoodpub.models import Read
from .utils import search_via_book_api
from .tasks import async_search_via_book_api


class BookAPIView(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    search_fields = ('title', 'author', 'pub_nm')
    filter_backends = (filters.SearchFilter,)

    @list_route(methods=['get'])
    def load(self, request, *args, **kwargs):
        if 'title' not in request.GET:
            return JsonResponse({'content': 'fail'})

        res = search_via_book_api(title=request.GET['title'])
        return JsonResponse({'content': res.content})

    @permission_classes((AllowAny, ))
    def list(self, request, *args, **kwargs):

        if 'search' in request.GET:
            keyword = request.GET['search'].encode('utf-8')
            search_keyword = cache.get('search_keyword')

            if not search_keyword:
                search_keyword = []
            if keyword not in search_keyword:
                search_keyword.append(keyword)
                async_search_via_book_api.delay(keyword)
                cache.set('search_keyword', search_keyword, 60 * 60)

        else:
            books_for_anonoymous = cache.get('books_for_anonoymous')
            if not books_for_anonoymous:
                books_for_anonoymous = list(Read.objects.values_list(
                    'book', flat=True).annotate(
                        total_count=Count('book')).order_by(
                            '-total_count')[:300])
                cache.set('books_for_anonoymous', books_for_anonoymous,
                          60 * 60 * 6)
            self.queryset = self.get_queryset().filter(
                isbn__in=set(books_for_anonoymous)).annotate(
                    total_count=Count('read')).order_by(
                        '-total_count')

        return super(BookAPIView, self).list(request, *args, **kwargs)


def book(request, book_id):
    template = loader.get_template('hoodpub/book.html')
    try:
        book = Book.objects.get(isbn=book_id)
    except Book.DoesNotExist:
        book = None
    context = RequestContext(request, {
        'book': book,
    })
    return HttpResponse(template.render(context))
