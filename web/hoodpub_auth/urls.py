from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
import views

urlpatterns = [
    url(r'^register_by_access_token/(?P<backend>[^/]+)/$',
        views.register_by_access_token),
]

urlpatterns = format_suffix_patterns(urlpatterns)
