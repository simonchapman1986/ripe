from django.db import models
from django_extensions.db.fields import UUIDField

import logging
import datetime


logger = logging.getLogger('reporting')


class CubeSubscriptionRevenueDaily(models.Model):
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

    # index
    id = UUIDField(version=4, primary_key=True)

    # dim_territory
    territory_code = models.CharField(max_length=10, default='')

    # dim_client
    client_id = models.CharField(max_length=36, default='')

    client_name = models.CharField(max_length=36, default='')

    # tran id
    transaction_id = models.CharField(max_length=36, default='')

    # dim subscription status
    subscription_status = models.CharField(max_length=255, default='')

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

    # bespoke values
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    card_suffix = models.CharField(max_length=255, default='')
    # dim user...?
    first_name = models.CharField(max_length=255, default='')
    last_name = models.CharField(max_length=255, default='')

    created = models.DateTimeField(auto_created=True, auto_now=True, default=datetime.datetime.now())

    class Meta:
        app_label = 'cubes'
        db_table = 'summary_subscription_revenue_daily'

    @classmethod
    def raw(cls, start, end, filters=None, group=None):
        """
        >>> c = CubeSubscriptionRevenueDaily()
        >>> start = end = datetime.datetime(2010, 01, 01).date()
        >>> r = c.get_data(start, end, {'client_id': '6e8bb589-fac1-11e3-a559-2c44fd1f0554'})
        >>> print [(k, v) for k, v in r[0].iteritems()] if len(r) else 'no data'
        """
        cls.raw_subs = CubeSubscriptionRevenueDaily.objects.all()
        cls.raw_subs = cls.raw_subs.filter(date__gte=start, date__lte=end)

        if filters:
            if 'client_id' in filters.keys():
                cls.raw_subs = cls.raw_subs.filter(client_id=filters['client_id'])
        return cls.raw_subs.values()

