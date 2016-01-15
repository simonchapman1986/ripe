from django.db import models
from django_extensions.db.fields import UUIDField

import logging
import datetime


logger = logging.getLogger('reporting')


class CubeDownload(models.Model):
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

    # dim_utc_date
    date = models.DateField()
    year = models.SmallIntegerField()
    month = models.SmallIntegerField()
    day = models.SmallIntegerField()
    day_of_week = models.IntegerField()
    day_name = models.CharField(max_length=9)
    week_of_year = models.SmallIntegerField()
    quarter = models.SmallIntegerField()

    # fact download
    product_id = UUIDField(version=4)
    asset_id = UUIDField(version=4)
    status = models.CharField(max_length=255)
    network = models.CharField(max_length=255, null=True)

    # agg data - not indexes - these are what we are after from the query
    total = models.IntegerField()
    total_new = models.IntegerField()
    average_per_day = models.IntegerField()
    breakdown_pct = models.IntegerField()

    created = models.DateTimeField(auto_created=True, auto_now=True, default=datetime.datetime.now())

    class Meta:
        app_label = 'cubes'
        db_table = 'summary_download_daily'
