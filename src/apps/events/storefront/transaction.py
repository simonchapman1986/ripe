from celery.task import task

from apps.events.storefront import SERVICE_NAME
from apps.events.event_tools import parse_args_as_json

from apps.base.models import FactServicesStorefrontTransaction
from apps.events.models import Log


@task()
@parse_args_as_json('{}.Transaction'.format(SERVICE_NAME))
def transaction(data):
    """
    Storefront: Transaction status report events


    item_id
    product_id
    window_id
    transaction_id
    transaction_status
    internal_user_id
    external_user_id
    account_id
    right_id
    price
    currency
    retail_model
    definition
    client_id
    territory
    platform_os
    platform_name
    platform_version
    device_id
    mnc (optional)
    mcc (optional)
    last_4_digits
    event_time
    """
    logs = Log.create_flag(event_name='transaction', packet=data)
    FactServicesStorefrontTransaction.create_fact(logs=logs, **data)
