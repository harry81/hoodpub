from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

from rest_framework import routers
from book import views as book_views
from hoodpub import views as hoodpub_views

router = routers.SimpleRouter()
router.register(r'api-book', book_views.BookAPIView, base_name="api-book")
router.register(r'api-user', hoodpub_views.UserProfileAPIView,
                base_name="api-user")
router.register(r'api-hoodpub', hoodpub_views.HoodpubAPIView,
                base_name="api-hoodpub")
router.register(r'api-comment', hoodpub_views.CommentAPIView,
                base_name="api-comment")


urlpatterns = patterns('',
     url(r'^$', hoodpub_views.index),
     url(r'^book/(?P<book_id>[0-9a-zA-Z]+)/$', book_views.book),
     url(r'^', include(router.urls)),
     url(r'^hoodpub-auth/', include('hoodpub_auth.urls')),
     url(r'^api-token-auth/', 'rest_framework_jwt.views.obtain_jwt_token'),
     url(r"^auth/", include('rest_framework_social_oauth2.urls')),
     url(r'^admin/', include(admin.site.urls)),
     url(r'^docs/', include('rest_framework_swagger.urls')),
 )

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
