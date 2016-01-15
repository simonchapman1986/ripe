from django.conf.urls import patterns
from django.conf.urls import url


urlpatterns = patterns(
    '',

    url(r'^(?P<client>(.)*)'
        r'/(?P<report_name>(registrations))'
        r'/(?P<group>(.)*)'
        r'/total/'
        r'(?P<territory>(.)*)'
        r'/(?P<platform>(.)*)'
        r'/(?P<start_date>(.)*)'
        r'/(?P<end_date>(.)*)/$',
        'apps.api.views.v1.registration.registration_report',
        {"interval": "total"}
        ),

    url(r'^(?P<client>(.)*)'
        r'/(?P<report_name>(registrations))'
        r'/(?P<group>(.)*)'
        r'/monthly/'
        r'(?P<territory>(.)*)'
        r'/(?P<platform>(.)*)'
        r'/(?P<start_date>(.)*)'
        r'/(?P<end_date>(.)*)/$',
        'apps.api.views.v1.registration.registration_report',
        {"interval": "monthly"}
        ),

    url(r'^(?P<client>(.)*)'
        r'/(?P<report_name>(registrations))'
        r'/(?P<group>(.)*)'
        r'/weekly/'
        r'(?P<territory>(.)*)'
        r'/(?P<platform>(.)*)'
        r'/(?P<start_date>(.)*)'
        r'/(?P<end_date>(.)*)/$',
        'apps.api.views.v1.registration.registration_report',
        {"interval": "weekly"}
        ),

    url(r'^(?P<client>(.)*)'
        r'/(?P<report_name>(registrations))'
        r'/(?P<group>(.)*)'
        r'/daily/'
        r'(?P<territory>(.)*)'
        r'/(?P<platform>(.)*)'
        r'/(?P<start_date>(.)*)'
        r'/(?P<end_date>(.)*)/$',
        'apps.api.views.v1.registration.registration_report',
        {"interval": "daily"}
        ),

)

