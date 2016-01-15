from django.db import models
from django_extensions.db.fields import UUIDField
from apps.base.models.facts.services.storefront.tools.fact_tools import exists
from apps.base.models.facts.services.storefront.tools.fact_tools import save_user
from apps.base.models.facts.services.storefront.tools.fact_tools import save_platform
from apps.br.subscription import get_rule
from apps.br.subscription import RNS
from apps.base.models.dimensions.dimension_platform import DimensionPlatform
from apps.base.models.dimensions.dimension_subscription_status import DimensionSubscriptionStatus as DSS
from apps.base.models.dimensions.dimension_subscription_state import DimensionSubscriptionState as DSSe
from apps.base.models.dimensions.dimension_subscription_type import DimensionSubscriptionType as DST
from apps.base.models.dimensions.dimension_utc_date import DimensionUTCDate
from apps.base.models.dimensions.dimension_client import DimensionClient
from apps.base.models.dimensions.dimension_territory import DimensionTerritory
from apps.base.models.dimensions.dimension_user import DimensionUser
from apps.base.models.dimensions.dimension_window import DimensionWindow
from apps.base.models.dimensions.dimension_item import DimensionItem
from apps.base.models.dimensions.dimension_product import DimensionProduct
from apps.base.models.dimensions.dimension_right import DimensionRight

import datetime

import logging
log = logging.getLogger('reporting')


class FactServicesStorefrontSubscription(models.Model):
    """
    FactServicesStorefrontSubscription

    The fact for storefront subscription events.


    This model is used to store our incoming events from the storefront service for subscriptions.
    We treat this model for one use alone, and thats to log every event.

    The fact has multi-dimensions which we later use to summarise this data.

    Each dimension MUST be added to allow use to cube our information for general aggregated use.
    """

    user = models.ForeignKey(DimensionUser, null=True, default=None)
    subscription_id = UUIDField(version=4, null=True, default=None)
    subscription_type = models.ForeignKey(DST, null=True, default=None)
    subscription_status = models.ForeignKey(DSS, null=True, default=None)
    subscription_state = models.ForeignKey(DSSe, null=True, default=None)
    subscription_state_error = models.BooleanField(default=False, db_index=True)
    platform = models.ForeignKey(DimensionPlatform, null=True, default=None)
    window = models.ForeignKey(DimensionWindow, null=True, default=None)
    transaction_id = models.CharField(max_length=255, null=True, default=None)
    event_utc_date = models.ForeignKey(DimensionUTCDate, null=True, default=None)
    event_utc_datetime = models.DateTimeField(null=True, default=None)
    last_modified_utc = models.DateTimeField(auto_now_add=True, auto_now=True)

    class Meta:
        app_label = 'base'
        db_table = 'fact_services_storefront_subscriptions'

    @classmethod
    def get_last_event(cls, subscription_id, date=datetime.datetime.now()):
        try:
            last = FactServicesStorefrontSubscription.objects.filter(subscription_id=subscription_id).exclude(
                event_utc_datetime__gte=date).order_by('-event_utc_datetime')

            return last[0].subscription_state.state
        except:
            return RNS

    @classmethod
    def create_fact(cls, logs, **data):
        # dims
        platform = save_platform(data, event='Storefront Subscription')

        territory = DimensionTerritory.insert(code=data['territory']) if exists('territory', data) else None

        client = DimensionClient.insert(client_id=data['client_id']) if exists('client_id', data) else None

        du = save_user(data, territory, client, event='Storefront Subscription')

        dst = DST.insert(
            period=data['subscription_period'] if exists('subscription_period', data) else None,
            recurrence=data['subscription_recurrence'] if exists('subscription_recurrence', data) else None
        ) if any([d in data for d in ['subscription_period', 'subscription_recurrence']]) else None

        dss_status, _ = DSS.insert(event=int(data['subscription_status'])) if exists('subscription_status', data) else None

        state, err = get_rule(
            status=data.get('subscription_status', None),
            current_state=FactServicesStorefrontSubscription.get_last_event(
                subscription_id=data.get('subscription_id', None)
            ),
            window_ongoing=bool(data.get('window_on_going', False))
        )

        dsse, _ = DSSe.objects.get_or_create(state=state)

        item = DimensionItem.insert(item_id=data.get('item_id')) if exists('item_id', data) else None
        product = DimensionProduct.insert(product_id=data.get('product_id')) if exists('product_id', data) else None
        usage_right = DimensionRight.insert(
            right_id=data.get('window_usage_right_id')
        ) if exists('window_usage_right_id', data) else None

        window = DimensionWindow.insert(
            window_id=data.get('window_id', None),
            item=item,
            product=product,
            start_date=data['window_start_date'],
            end_date=data['window_end_date'],
            pricing_id=data['window_pricing_id'],
            usage_right_id=usage_right,
            tier=data['window_tier'],
            deleted=data['window_deleted_date'],
            window_type=data['window_type'],
            on_going=data['window_on_going'],
            repeat_count=data['window_repeat_count'],
            auto_upgrade=data['window_auto_upgrade'],
            allow_repurchase=data['window_allow_repurchase'],
            apple_product_id=data['apple_product_id'],
        )if any([i in data for i in [
            'window_id',
            'item_id',
            'product_id',
            'window_start_date',
            'window_end_date',
            'window_pricing_id',
            'window_usage_right_id',
            'window_tier',
            'window_deleted_date',
            'window_type',
            'window_on_going',
            'window_repeat_count',
            'window_auto_upgrade',
            'window_allow_repurchase',
            'apple_product_id',
        ]]) else None

        # fact create
        fact = FactServicesStorefrontSubscription.objects.create(
            user=du,
            subscription_id=data.get('subscription_id', None),
            subscription_type=dst,
            subscription_status=dss_status,
            subscription_state=dsse,
            subscription_state_error=err,
            platform=platform,
            window=window,
            transaction_id=data.get('transaction_id', None),
            event_utc_date=DimensionUTCDate.date_from_datetime(datetime=data['event_time']),
            event_utc_datetime=data.get('event_time', None)
        )

        try:
            FactServicesStorefrontSubscription.objects.get(pk=fact.pk)
            exist = True
        except FactServicesStorefrontSubscription.DoesNotExist:
            exist = False

        logs.completed = exist
        logs.save()