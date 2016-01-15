from django.db import models
from django_extensions.db.fields import UUIDField

import logging
import datetime


logger = logging.getLogger('reporting')


class CubeContent(models.Model):
    """
    indexes sit on the values we will be filtering on
    these indexes are relational to the dim tables from
    which the aggregated data derives
    """
    
    # index
    id = UUIDField(version=4, primary_key=True)

    # dim_client
    client_id = models.CharField(max_length=36)

    # dim_studio
    content_provider = models.CharField(max_length=255)

    # dim_assets
    asset_role_type = models.CharField(max_length=255)

    # ... TODO
    mezzanine_delivery_date = models.DateField(null=True)

    # dim_definition
    definition = models.CharField(max_length=255)

    # dim_language
    language = models.CharField(max_length=3)

    # dim_utc_date
    date = models.DateField()
    year = models.SmallIntegerField()
    month = models.SmallIntegerField()
    day = models.SmallIntegerField()
    day_of_week = models.IntegerField()
    day_name = models.CharField(max_length=9)
    week_of_year = models.SmallIntegerField()
    quarter = models.SmallIntegerField()

    # fact agg
    file_size = models.BigIntegerField(max_length=10)
    duration_of_asset = models.IntegerField(max_length=10, default='')

    title = models.CharField(max_length=255)
    added_to_client = models.DateField(null=True)

    created = models.DateTimeField(auto_created=True, auto_now=True, default=datetime.datetime.now())

    class Meta:
        app_label = 'cubes'
        db_table = 'summary_content_daily'
