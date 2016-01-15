from django.conf.urls import patterns
from django.conf.urls import url


urlpatterns = patterns(
    '',
    # subscription total report
    url(r'^(?P<client>(.)*)/'                   # client        | client id     1
        r'subscriptions/'                       # report name   | our report    2
        r'(?P<package>(.)*)/'                   # package       | filter        3
        r'(?P<state>(.)*)/'                     # state         | filter        4
        r'(?P<group>(.)*)/'                     # group         | group by      5
        r'total/'                               # total         | type          6
        r'(?P<territory>(.)*)/'                 # territory     | filter        7
        r'(?P<platform>(.)*)/'                  # platform      | filter        8
        r'(?P<start_date>(.)*)/'                # start date    | filter        9
        r'(?P<end_date>(.)*)/$',                # end date      | filter        10
        'apps.api.views.v1.user_subscription.total_subscription_report'),

    url(r'^(?P<client>(.)*)/(?P<report_name>(subscriptions))/(?P<package>(.)*)/(?P<state>(.)*)/(?P<group>(.)*)/monthly/'
        r'(?P<territory>(.)*)/(?P<platform>(.)*)/(?P<start_date>(.)*)/(?P<end_date>(.)*)/$',
        'apps.api.views.v1.user_subscription.total_subscription_report', {"interval": "monthly"}),

    url(r'^(?P<client>(.)*)/(?P<report_name>(subscriptions))/(?P<package>(.)*)/(?P<state>(.)*)/(?P<group>(.)*)/weekly/'
        r'(?P<territory>(.)*)/(?P<platform>(.)*)/(?P<start_date>(.)*)/(?P<end_date>(.)*)/$',
        'apps.api.views.v1.user_subscription.total_subscription_report', {"interval": "weekly"}),

    url(r'^(?P<client>(.)*)/(?P<report_name>(subscriptions))/(?P<package>(.)*)/(?P<state>(.)*)/(?P<group>(.)*)/daily/'
        r'(?P<territory>(.)*)/(?P<platform>(.)*)/(?P<start_date>(.)*)/(?P<end_date>(.)*)/$',
        'apps.api.views.v1.user_subscription.total_subscription_report', {"interval": "daily"}),



    #url(r'^(?P<client>(.)*)/(?P<report_name>(subscriptions))/(?P<group>(.)*)/total/(?P<territory>(.)*)/(?P<platform>(.)*)/(?P<package>(.)*)/(?P<state>(.)*)/(?P<provider>(.)*)/(?P<start_date>(.)*)/(?P<grain_count>(.)*)/$', 'apps.api.views.v1.user_subscription.total_subscription_report'),
    #url(r'^(?P<client>(.)*)/(?P<report_name>(subscriptions))/(?P<group>(.)*)/monthly/(?P<territory>(.)*)/(?P<platform>(.)*)/(?P<package>(.)*)/(?P<state>(.)*)/(?P<provider>(.)*)/(?P<start_date>(.)*)/(?P<grain_count>(.)*)/$', 'apps.api.views.v1.user_subscription.monthly_subscription_report'),
    #url(r'^(?P<client>(.)*)/(?P<report_name>(subscriptions))/(?P<group>(.)*)/weekly/(?P<territory>(.)*)/(?P<platform>(.)*)/(?P<package>(.)*)/(?P<state>(.)*)/(?P<provider>(.)*)/(?P<start_date>(.)*)/(?P<grain_count>(.)*)/$', 'apps.api.views.v1.user_subscription.weekly_subscription_report'),
    #url(r'^(?P<client>(.)*)/(?P<report_name>(subscriptions))/(?P<group>(.)*)/daily/(?P<territory>(.)*)/(?P<platform>(.)*)/(?P<package>(.)*)/(?P<state>(.)*)/(?P<provider>(.)*)/(?P<start_date>(.)*)/(?P<grain_count>(.)*)', 'apps.api.views.v1.user_subscription.daily_subscription_report'),
)
