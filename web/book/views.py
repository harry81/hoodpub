from django.http import JsonResponse

from rest_framework import viewsets
from rest_framework import filters
from rest_framework.decorators import list_route

from .serializers import BookSerializer
from .models import Books
from .utils import search_via_book_api
from .tasks import async_search_via_book_api


class BookAPIView(viewsets.ModelViewSet):
    queryset = Books.objects.all().order_by('-cover_l_url')
    serializer_class = BookSerializer
    search_fields = ('title', 'description', 'author', 'pub_nm')
    filter_backends = (filters.SearchFilter,)

    @list_route(methods=['get'])
    def load(self, request, *args, **kwargs):
        if 'title' not in request.GET:
            return JsonResponse({'content': 'fail'})

        res = search_via_book_api(title=request.GET['title'])
        return JsonResponse({'content': res.content})

    def list(self, request, *args, **kwargs):
        if 'search' in request.GET:
            async_search_via_book_api.delay(
                request.GET['search'].encode('utf-8'))
        return super(BookAPIView, self).list(request, *args, **kwargs)
