from celery.task import task

from apps.events.storefront import SERVICE_NAME
from apps.events.event_tools import parse_args_as_json

from apps.base.models import FactServicesStorefrontDownload


@task()
@parse_args_as_json('{}.Download'.format(SERVICE_NAME))
def download(data):
    """
    Storefront: User Registration event injection


    internal_user_id
    external_user_id
    client_id
    item_id
    device_id
    product_id
    asset_id
    status
    network
    expiry_date
    event_time
    """
    FactServicesStorefrontDownload.create_fact(**data)
