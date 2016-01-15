from celery.task import task

from apps.events.aggregator import SERVICE_NAME
from apps.events.event_tools import parse_args_as_json

from apps.base.models import FactServicesLicensingDelivery


@task()
@parse_args_as_json('{}.Aggregation'.format(SERVICE_NAME))
def delivery(data):
    """
    Licensing: Delivery add

    client_id
    external_user_id
    device_id
    drm_type
    transaction_id
    event_time
    """
    FactServicesLicensingDelivery.create_fact(**data)