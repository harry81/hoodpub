from django.conf.urls import patterns, include, url
from django.contrib import admin

from rest_framework import routers
from book import views as book_views
from hoodpub import views as hoodpub_views

router = routers.SimpleRouter()
router.register(r'api-book', book_views.BookAPIView, base_name="api-book")
router.register(r'api-user', hoodpub_views.UserProfileAPIView,
                base_name="api-user")
router.register(r'api-hoodpub', hoodpub_views.HoodpubAPIView,
                base_name="api-hoodpub")


urlpatterns = patterns('',
     url(r'^$', hoodpub_views.index),
     url(r'^', include(router.urls)),
     url(r'^hoodpub-auth/', include('hoodpub_auth.urls')),
     url(r"^auth/", include('rest_framework_social_oauth2.urls')),
     url(r'^admin/', include(admin.site.urls)),
     url(r'^docs/', include('rest_framework_swagger.urls')),
 )
