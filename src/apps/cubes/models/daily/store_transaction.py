from django.db import models
from django_extensions.db.fields import UUIDField
from apps.base.models.data import BLANK_UUID

import logging
import datetime


log = logging.getLogger('reporting')


class CubeStoreTransaction(models.Model):
    """
    indexes sit on the values we will be filtering on
    these indexes are relational to the dim tables from
    which the aggregated data derives
    """
    
    # index
    id = UUIDField(version=4, primary_key=True)

    # dim_territory
    territory_code = models.CharField(max_length=10)

    # dim_client
    client_id = models.CharField(max_length=36)
    client_name = models.CharField(max_length=36, default='')

    # dim_utc_date
    date = models.DateField()
    year = models.SmallIntegerField()
    month = models.SmallIntegerField()
    day = models.SmallIntegerField()
    day_of_week = models.IntegerField()
    day_name = models.CharField(max_length=9)
    week_of_year = models.SmallIntegerField()
    quarter = models.SmallIntegerField()

    # dim_item
    item_id = UUIDField(version=4)
    item_title = models.CharField(max_length=255L, blank=True, null=True)
    content_type = models.CharField(max_length=30L, blank=True, null=True)

    #dim_user
    external_user_id = UUIDField(version=4, default=BLANK_UUID)
    first_name = models.CharField(max_length=255, blank=True, null=True, default='')
    last_name = models.CharField(max_length=255, blank=True, null=True, default='')


    # dim_windowr
    window_id = UUIDField(version=4)

    # dim_product
    product_id = UUIDField(version=4)

    # dim_transaction_status
    transaction_status = models.CharField(max_length=255)

    # dim_right
    right_id = models.CharField(max_length=255, null=True)

    # dim_currency
    currency_code = models.CharField(max_length=10)

    # dim_retail_model
    retail_model = models.CharField(max_length=255, null=True, blank=True)

    # dim_definition
    definition = models.CharField(max_length=255)

    # dim_device
    device_id = UUIDField(version=4)

    last_4_digits = models.CharField(max_length=4, null=True, default='')

    # dim_platform
    platform_os = models.CharField(max_length=255)
    platform_name = models.CharField(max_length=255)
    platform_version = models.CharField(max_length=255)

    # fact store transaction
    mnc = models.CharField(max_length=255, null=True)
    mcc = models.CharField(max_length=255, null=True)

    # agg data - not indexes - these are what we are after from the query
    total = models.IntegerField()
    total_new = models.IntegerField()
    average_per_day = models.IntegerField()
    breakdown_pct = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total_price_day = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    created = models.DateTimeField(auto_created=True, auto_now=True, default=datetime.datetime.now())

    class Meta:
        app_label = 'cubes'
        db_table = 'summary_storetransaction_daily'


    @classmethod
    def get_data(cls, start, end, filters=None, group=None):
        """
        >>> c = CubeStoreTransaction()
        >>> start = end = datetime.datetime(2010, 01, 01).date()
        >>> r = c.get_data(start, end, {'client_id': '6e8bb589-fac1-11e3-a559-2c44fd1f0554'})
        >>> print [(k, v) for k, v in r[0].iteritems()] if len(r) else 'no data'
        """
        cls.transactions = CubeStoreTransaction.objects.all()
        cls.transactions = cls.transactions.filter(date__gte=start, date__lte=end)

        if filters:
            if 'client_id' in filters.keys():
                cls.transactions = cls.transactions.filter(client_id=filters['client_id'])
        return cls.transactions.values()
