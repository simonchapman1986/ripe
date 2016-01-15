from django.conf.urls import patterns, include

from tastypie.api import Api

from apps.api.resources import RegistrationResource


registation = Api('registration')
registation.register(RegistrationResource())


urlpatterns = patterns(
    '',
    (r'^logs/v1/', include(registation.urls)),
)
