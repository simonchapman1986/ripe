from django.db import models
from django_extensions.db.fields import UUIDField

import logging
import datetime
# from apps.cubes.models.daily.managers.subscriptions import SubscriptionManager


logger = logging.getLogger('reporting')


class CubeSubscriptionsDaily(models.Model):
    """
    indexes sit on the values we will be filtering on
    these indexes are relational to the dim tables from
    which the aggregated data derives

    DO NOT add indexes to any of these rows using the conventional django method.
    They have been specifically added via South to enable the choice of INDEX type
    In this case the majority of the required indexes are HASH due to only matching exact.
    The cases where equality is required, have BTREE indexes applied (mainly date related).

    Please see the initial cube migration for further reference on the indexing of
    this table, and how to follow suit to add/delete/alter if and when required for
    future migrations.
    """

    objects = models.Manager()
    #subscriptions = SubscriptionManager()

    # index
    id = UUIDField(version=4, primary_key=True)

    # dim_territory
    territory_code = models.CharField(max_length=10, default='')

    # dim_client
    client_id = models.CharField(max_length=36, default='')

    # dim window
    window_item_id = models.CharField(max_length=255, default='')
    window_product_id = models.CharField(max_length=255, default='')
    window_pricing_id = models.CharField(max_length=255, default='')
    window_usage_right_id = models.CharField(max_length=255, default='')
    window_tier = models.CharField(max_length=255, default='')
    window_type = models.CharField(max_length=255, default='')
    window_on_going = models.BooleanField(default=False)
    window_repeat_count = models.SmallIntegerField(default=0)
    window_auto_upgrade = models.BooleanField(default=False)
    window_allow_repurchase = models.BooleanField(default=False)

    # dim subscription status
    subscription_status = models.CharField(max_length=255, default='')

    # dim subscription state
    subscription_state = models.CharField(max_length=255, default='')
    subscription_state_error = models.BooleanField(default=False)

    # dim_utc_date
    date = models.DateField()
    year = models.SmallIntegerField()
    month = models.SmallIntegerField()
    day = models.SmallIntegerField()
    day_of_week = models.IntegerField()
    day_name = models.CharField(max_length=9)
    week_of_year = models.SmallIntegerField()
    quarter = models.SmallIntegerField()

    # dim_platform
    os = models.CharField(max_length=255, default='')
    name = models.CharField(max_length=255, default='')
    version = models.CharField(max_length=255, default='')

    # agg data - not indexes - these are what we are after from the query
    total = models.IntegerField()
    total_new = models.IntegerField()
    average_per_day = models.IntegerField()
    change = models.IntegerField()
    breakdown_pct = models.IntegerField()

    created = models.DateTimeField(auto_created=True, auto_now=True, default=datetime.datetime.now())

    class Meta:
        app_label = 'cubes'
        db_table = 'summary_subscriptions_daily'

    @classmethod
    def test(cls):
        return 'refactor me'
