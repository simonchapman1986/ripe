from django.conf.urls import patterns, include

from tastypie.api import Api

from apps.api.resources import SubscriptionResource


subscription = Api('subscription')
subscription.register(SubscriptionResource())


urlpatterns = patterns(
     '',
     (r'^logs/v1/', include(subscription.urls)),
)
