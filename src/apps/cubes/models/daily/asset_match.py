from django.db import models

from django_extensions.db.fields import UUIDField

from apps.base.models.dimensions.dimension_item_provider import DimensionItemProvider
import datetime
from django.conf import settings

import logging
log = logging.getLogger('reporting')


class CubeAssetMatch(models.Model):

    """
    indexes sit on the values we will be filtering on
    these indexes are relational to the dim tables from
    which the aggregated data derives
    """

    # index
    id = UUIDField(version=4, primary_key=True)

    # dim_client
    client_id = models.CharField(max_length=36)
    client_name = models.CharField(max_length=36)

    # dim_territory
    territory_code = models.CharField(max_length=10)

    # dim item
    item_id = UUIDField(version=4)
    item_content_type = models.CharField(max_length=30L, blank=True, null=True)
    item_title = models.CharField(max_length=255L, blank=True, null=True)
    item_release_year = models.IntegerField(null=True, blank=True)
    item_runtime = models.CharField(max_length=8L, blank=True, null=True)
    item_duration = models.IntegerField(null=True, blank=True)
    item_last_modified = models.DateTimeField(null=True, blank=True)

    # dim assets
    asset_id = models.CharField(max_length=255, unique=True)
    asset_type = models.CharField(max_length=255)

    # dim role
    data_role = models.CharField(max_length=255)

    # dim processing state
    processing_state = models.CharField(max_length=255)

    # dim used assets
    used_asset_ids = models.TextField()  # stored as json {id: type}

    # dim item provider
    item_provider_id = models.CharField(max_length=128L, blank=True, null=True)
    item_provider_name = models.CharField(max_length=128L, blank=True, null=True)

    # dim definition
    definition = models.CharField(max_length=255, null=True, blank=True)

    # dim languages
    languages_iso_code = models.TextField()  # stored as json {int: iso}

    file_size = models.BigIntegerField(max_length=10)
    duration = models.IntegerField(max_length=10, default='')
    spec_name = models.CharField(max_length=128, null=True, blank=True)
    delivery_date = models.DateTimeField(default=None)

    # dim_utc_date
    date = models.DateField()
    year = models.SmallIntegerField()
    month = models.SmallIntegerField()
    day = models.SmallIntegerField()
    day_of_week = models.IntegerField()
    day_name = models.CharField(max_length=9)
    week_of_year = models.SmallIntegerField()
    quarter = models.SmallIntegerField()

    created = models.DateTimeField(auto_created=True, auto_now=True, default=datetime.datetime.now())

    class Meta:
        app_label = 'cubes'
        db_table = 'summary_asset_match_daily'

    @classmethod
    def get_data(cls,  start, end, filters=None, group=None):

        cls.filter_content_data(start, end, filters=filters)

        if not len(cls.data):
            log.debug('NO CONTENT DATA AVAILABLE FOR GIVEN FILTERS. start-date: {} end-date: {}'.format(
                start.strftime(settings.DATE_FORMAT_YMD), end.strftime(settings.DATE_FORMAT_YMD))
            )
            return None

        return cls.data.values()

    @classmethod
    def filter_content_data(cls, start, end, filters=None):
        cls.data = CubeAssetMatch.objects.all()
        cls.data = cls.data.filter(date__gte=start).filter(date__lte=end)

        if isinstance(filters, dict):
            if len(cls.data) and len(filters):
                keys = filters.keys()
                if 'client_id' in keys:
                    cls.data = cls.data.filter(client_id=filters['client_id'])
            else:
                log.info('---------No cube data found after applying date filters and/or no extra filters present.')
        else:
            raise Exception('---------Unexpected filters format. {}'.format(type(filters)))

