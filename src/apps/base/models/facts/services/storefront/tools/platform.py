from django.db.models import Q

from apps.base.models.dimensions.dimension_platform import DimensionPlatform


def get_platform(local_data, model):
    valid_keys = all(
        [i in local_data
         for i in ['platform_os', 'platform_name', 'platform_version']])
    if valid_keys:
        return DimensionPlatform.insert(
            os=local_data['platform_os'],
            name=local_data['platform_name'],
            version=local_data['platform_version'])

    fact_record = model.objects.filter(
        ~Q(platform_id=-1),
         subscription_id=local_data['subscription_id'])
    if fact_record.count() == 0:
        return DimensionPlatform.objects.get(id=-1)

    # always use the first record here
    return fact_record[0].platform