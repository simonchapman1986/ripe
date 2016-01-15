from celery.task import task
from apps.events.storefront import SERVICE_NAME
from apps.events.event_tools import parse_args_as_json
from apps.base.models import FactServicesStorefrontSubscription
from apps.events.models import Log


import logging
log = logging.getLogger('reporting')


@task()
@parse_args_as_json('{}.Subscription'.format(SERVICE_NAME))
def user_subscription(data):
    """
    Storefront: User Subscription event injection

    window_id
    item_id
    product_id
    window_start_date
    window_end_date
    window_pricing_id
    window_usage_right_id
    window_tier
    window_deleted_date
    window_type
    window_on_going
    window_repeat_count
    window_auto_upgrade
    window_allow_repurchase
    apple_product_id
    transaction_id
    internal_user_id
    external_user_id
    territory
    client_id
    subscription_id
    subscription_period
    subscription_recurrence
    subscription_status
    platform_os
    platform_name
    platform_version
    event_time
    >>> from uuid import uuid4
    >>> from django.utils import timezone
    >>> iuid = unicode(uuid4())
    >>> euid = unicode(uuid4())
    >>> territory = u'GB'
    >>> cid = unicode(uuid4())
    >>> sid = unicode(uuid4())
    >>> sp = u'P1M'
    >>> sr = u'1'
    >>> ss = u'1'
    >>> et = unicode(timezone.now().isoformat())
    >>> data = {'internal_user_id': iuid, 'external_user_id': euid, 'territory': territory, 'client_id': cid, 'subscription_id': sid, 'subscription_period': sp, 'subscription_recurrence': sr, 'subscription_status': ss, 'event_time': et}
    >>> import json
    >>> data = json.dumps(data)
    >>> user_subscription(data)
    1
    """
    logs = Log.create_flag(event_name='user_subscription', packet=data)
    FactServicesStorefrontSubscription.create_fact(logs=logs, **data)
