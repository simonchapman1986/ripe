from django.conf.urls import patterns
from django.conf.urls import url

urlpatterns = patterns(
    'apps.api.views.v1.common',

    url(r'^check_instance/?$', 'check_instance'),
    url(r'^monitor_instance/?$', 'monitor_instance'),

)
