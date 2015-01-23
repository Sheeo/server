from django.conf.urls import patterns, include, url

from django.contrib import admin

from server.apps.authentication import urls

urlpatterns = patterns('',
    url(r'^', include(urls.urlpatterns)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth/', include('oauth2_provider.urls', namespace='oauth2_provider'))
)
