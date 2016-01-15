from django.db import models
from django_extensions.db.fields.json import JSONField

from apps.base.models.dimensions.dimension_utc_date import DimensionUTCDate
from apps.base.models.dimensions.dimension_item_provider import DimensionItemProvider
from apps.base.models.dimensions.dimension_item import DimensionItem
from apps.base.models.dimensions.dimension_language import DimensionLanguage
from apps.base.models.dimensions.dimension_vendor import DimensionVendor
from apps.base.models.dimensions.dimension_metadata_type import DimensionMetadataType
from apps.base.models.dimensions.dimension_metadata_country_origin import DimensionCountryCode


class FactServicesBackstageItemMetadata(models.Model):

    item_meta = models.ForeignKey(DimensionItem, default=-1)
    metadata_id = models.CharField(max_length=255, null=True, blank=True)
    version = models.CharField(max_length=16, null=True, blank=True)
    country_of_origin = models.ForeignKey(DimensionCountryCode)
    title = models.CharField(max_length=256, null=True, blank=True)
    copyright_cline = models.CharField(max_length=128, null=True, blank=True)
    provider = models.ForeignKey(DimensionItemProvider, null=True, blank=True)
    type = models.ForeignKey(DimensionMetadataType)
    isan = models.CharField(max_length=36, null=True, blank=True)
    eidr = models.CharField(max_length=36, null=True, blank=True)
    genres = JSONField(default={}, blank=True)
    release_date = models.DateField(null=True, blank=True)
    production_company = models.CharField(max_length=128, null=True, blank=True)
    release_year = models.CharField(max_length=16, null=True, blank=True)
    primary_language = models.ForeignKey(DimensionLanguage, null=True, blank=True)
    short_synopsis = models.TextField(null=True, blank=True)
    medium_synopsis = models.TextField(null=True, blank=True)
    long_synopsis = models.TextField(null=True, blank=True)
    runtime = models.CharField(max_length=8, null=True, blank=True)
    vendor = models.ForeignKey(DimensionVendor)
    episode_number = models.IntegerField(null=True, blank=True)
    season = models.CharField(max_length=255, null=True, blank=True)
    show_title = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(default=None)
    modified = models.DateTimeField(default=None)
    original_url = models.CharField(max_length=255, null=True, blank=True)
    ultraviolet = models.BooleanField(default=False)

    event_utc_date = models.ForeignKey(DimensionUTCDate)
    event_utc_datetime = models.DateTimeField()
    last_modified_utc = models.DateTimeField(auto_now_add=True, auto_now=True)

    class Meta:
        app_label = 'base'
        db_table = 'fact_services_backstage_item_metadata'

    @classmethod
    def create_fact(cls, **data):
        dip = DimensionItemProvider.insert(
            True,
            provider_id=data['provider_id'],
            provider_name=data['provider_name'],
        )
        pl = DimensionLanguage.insert(iso_code=data['primary_language'])
        vendor = DimensionVendor.insert(name=data['vendor'])
        country = DimensionCountryCode.objects.get(iso_code=data['country_of_origin_iso'])
        meta_type = DimensionMetadataType.insert(type=data['type'])
        item = DimensionItem.insert(item_id=data['item_id'])

        f = FactServicesBackstageItemMetadata.objects.create(
            metadata_id=data['metadata_id'],
            version=data['version'],
            country_of_origin=country,
            title=data['title'],
            copyright_cline=data['copyright_cline'],
            provider=dip,
            type=meta_type,
            isan=data['isan'],
            eidr=data['eidr'],
            release_date=data['release_date'],
            production_company=data['production_company'],
            release_year=data['release_year'],
            primary_language=pl,
            short_synopsis=data['short_synopsis'],
            medium_synopsis=data['medium_synopsis'],
            long_synopsis=data['long_synopsis'],
            runtime=data['runtime'],
            vendor=vendor,
            episode_number=data['episode_number'] or None,
            season=data['season'] or None,
            show_title=data['show_title'] or None,
            created=data['created'],
            modified=data['modified'] or data['created'],
            original_url=data['original_url'],
            ultraviolet=data['ultraviolet'],
            event_utc_date=DimensionUTCDate.date_from_datetime(datetime=data['event_time']),
            event_utc_datetime=data['event_time']
        )

        f.item_meta.add(item)

        return f
