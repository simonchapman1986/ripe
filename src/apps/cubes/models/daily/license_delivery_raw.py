from django.db import models
from django_extensions.db.fields import UUIDField

import logging
import datetime


log = logging.getLogger('reporting')


class CubeLicenseDeliveryRawDaily(models.Model):
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

    # dim_utc_date
    date = models.DateField()
    year = models.SmallIntegerField()
    month = models.SmallIntegerField()
    day = models.SmallIntegerField()
    day_of_week = models.IntegerField()
    day_name = models.CharField(max_length=9)
    week_of_year = models.SmallIntegerField()
    quarter = models.SmallIntegerField()

    # dim user
    internal_user_id = models.CharField(max_length=255, default='')
    external_user_id = models.CharField(max_length=255, default='')

    # dim device
    device_id = UUIDField(version=4, unique=True)
    make = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    device_os = models.CharField(max_length=255)
    device_os_version = models.CharField(max_length=255)

    #dim platform
    platform_name = models.CharField(max_length=255, default='')

    # drm
    drm_type = models.CharField(max_length=255)

    # fact
    transaction_id = UUIDField(version=4)

    # dim item
    item_id = UUIDField(version=4)
    item_title = models.CharField(max_length=255, default='')

    created = models.DateTimeField(auto_created=True, auto_now=True, default=datetime.datetime.now())

    class Meta:
        app_label = 'cubes'
        db_table = 'summary_license_delivery_raw_daily'

    @classmethod
    def test(cls):
        return 'refactor me'

    @classmethod
    def raw(cls, start, end, filters=None, group=None):
        """
        >>> c = CubeLicenseDeliveryRawDaily()
        >>> start = end = datetime.datetime(2014, 06, 19).date()
        >>> r = c.raw(start, end)
        >>> print [i.id for i in r]
        """
        cls.licenses = CubeLicenseDeliveryRawDaily.objects.all()
        cls.licenses = cls.licenses.filter(date__gte=start, date__lte=end)

        if filters:
            if 'client_id' in filters.keys():
                cls.licenses = cls.licenses.filter(client_id=filters['client_id'])
        return cls.licenses.values()

