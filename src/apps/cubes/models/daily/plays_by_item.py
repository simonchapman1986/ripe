from django.db import models
from django_extensions.db.fields import UUIDField
from django_extensions.db.fields.json import JSONField

import logging
import datetime


logger = logging.getLogger('reporting')


class CubePlaysByItem(models.Model):
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
    
    # index
    id = UUIDField(version=4, primary_key=True)

    # dim_utc_date
    date = models.DateField()
    year = models.SmallIntegerField()
    month = models.SmallIntegerField()
    day = models.SmallIntegerField()
    day_of_week = models.IntegerField()
    day_name = models.CharField(max_length=9, )
    week_of_year = models.SmallIntegerField()
    quarter = models.SmallIntegerField()

    # fact
    item_id = models.CharField(max_length=36)
    status = models.CharField(max_length=255)
    territory_code = models.CharField(max_length=10)
    client_id = models.CharField(max_length=36)
    device_id = models.CharField(max_length=36)

    # item/meta
    metadata_id = models.CharField(max_length=255, null=True, blank=True, default='')
    item_title = models.CharField(max_length=255, null=True, blank=True, default='')
    item_provider_name = models.CharField(max_length=128L, blank=True, null=True, default='')
    item_isan = models.CharField(max_length=36, null=True, blank=True, default='')
    item_eidr = models.CharField(max_length=36, null=True, blank=True, default='')
    item_genres = JSONField(default={}, blank=True)
    item_release_date = models.CharField(max_length=24, null=True, blank=True, default='')
    item_production_company = models.CharField(max_length=128, null=True, blank=True, default='')
    item_release_year = models.CharField(max_length=16, null=True, blank=True, default='')
    item_primary_language = models.CharField(max_length=8, default='')
    item_runtime = models.CharField(max_length=8, null=True, blank=True, default='')
    item_vendor_name = models.CharField(max_length=255, default='')
    item_episode_number = models.IntegerField(null=True, blank=True, default=0)
    item_season = models.CharField(max_length=255, null=True, blank=True, default='')
    item_show_title = models.CharField(max_length=255, null=True, blank=True, default='')
    item_ultraviolet = models.BooleanField(default=False)

    # agg data - not indexes - these are what we are after from the query
    total_new = models.IntegerField()
    total = models.IntegerField()

    created = models.DateTimeField(auto_created=True, auto_now=True, default=datetime.datetime.now())

    class Meta:
        app_label = 'cubes'
        db_table = 'summary_plays_by_item_daily'




