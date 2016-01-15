from apps.base.models import FactServicesStorefrontRegistration

from tastypie.resources import ModelResource


class RegistrationResource(ModelResource):
    class Meta:
        queryset = FactServicesStorefrontRegistration.objects.all()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        resource_name = 'entry'
        filtering = {
            'event_time': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
        }