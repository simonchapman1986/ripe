from apps.base.models import FactServicesStorefrontSubscription

from tastypie.resources import ModelResource


class SubscriptionResource(ModelResource):

    class Meta:
        queryset = FactServicesStorefrontSubscription.objects.all()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        resource_name = 'entry'
        filtering = {
            'event_time': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
        }