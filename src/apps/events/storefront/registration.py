from celery.task import task

from apps.events.storefront import SERVICE_NAME
from apps.events.event_tools import parse_args_as_json
from apps.events.models import Log

from apps.base.models import FactServicesStorefrontRegistration

import logging
log = logging.getLogger('reporting')


@task()
@parse_args_as_json('{}.Registration'.format(SERVICE_NAME))
def user_registration(data):
    """
    Storefront: User Registration event injection


    internal_user_id
    external_user_id
    territory
    client_id
    platform_os
    platform_name
    platform_version
    device_id
    device_make
    device_model
    device_os
    device_os_version
    event_time
    """
    logs = Log.create_flag(event_name='user_registration', packet=data)
    FactServicesStorefrontRegistration.create_fact(logs=logs, **data)