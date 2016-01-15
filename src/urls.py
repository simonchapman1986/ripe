from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin


urlpatterns = patterns(
    '',
    # logs
    url(r'^api/', include('apps.api.urls.logs.v1.subscription')),
    url(r'^api/', include('apps.api.urls.logs.v1.registration')),

    # summaries
    #url(r'^api/v1/', include('apps.api.urls.summaries.v1.subscription')),
    url(r'^api/v1/', include('apps.api.urls.summaries.v1.registration')),
    # common
    url(r'^api/v1/', include('apps.api.urls.common.v1.instance')),
)

if settings.ADMIN_ENABLED:
    admin.autodiscover()
    urlpatterns += url(r'^admin/', include(admin.site.urls)),
