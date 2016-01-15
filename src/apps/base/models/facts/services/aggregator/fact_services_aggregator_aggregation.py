from django.db import models

from apps.base.models.dimensions.dimension_utc_date import DimensionUTCDate
from apps.base.models.dimensions.dimension_item import DimensionItem
from apps.base.models.dimensions.dimension_job_manager import DimensionJobManager
from apps.base.models.dimensions.dimension_assets import DimensionAssets
from apps.base.models.dimensions.dimension_definition import DimensionDefinition
from apps.base.models.dimensions.dimension_language import DimensionLanguage
from apps.base.models.dimensions.dimension_client import DimensionClient
from apps.base.models.dimensions.dimension_vendor import DimensionVendor
from apps.base.models.dimensions.dimension_studio_item import DimensionStudioItem
from apps.base.models.dimensions.dimension_studio import DimensionStudio
from apps.base.models.dimensions.dimension_data_role import DimensionDataRole
from apps.base.models.dimensions.dimension_audio_channels import DimensionAudioChannels


class FactServicesAggregatorAggregation(models.Model):

    asset = models.ForeignKey(DimensionAssets, default=-1)
    unique_studio_item = models.ForeignKey(DimensionStudioItem, default=-1)
    studio = models.ForeignKey(DimensionStudio, default=-1)
    file_name = models.CharField(max_length=255, default='')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    file_size = models.BigIntegerField(max_length=10)
    checksum = models.CharField(max_length=255, default='')
    data_role = models.ForeignKey(DimensionDataRole, default=-1)
    content_duration = models.IntegerField(max_length=10, default='')
    definition = models.ForeignKey(DimensionDefinition, default=-1)
    language = models.ForeignKey(DimensionLanguage, default=-1)
    audio_channel = models.ForeignKey(DimensionAudioChannels, default=-1)
    client = models.ForeignKey(DimensionClient, default=-1)
    vendor = models.ForeignKey(DimensionVendor, default=-1)

    event_utc_date = models.ForeignKey(DimensionUTCDate)
    event_utc_datetime = models.DateTimeField()
    last_modified_utc = models.DateTimeField(auto_now_add=True, auto_now=True)

    class Meta:
        app_label = 'base'
        db_table = 'fact_services_aggregator_aggregation'

    @classmethod
    def create_fact(cls, **data):
        asset = DimensionAssets.insert(
            asset_id=data['asset_id'],
            type=data['asset_type']
        )

        unique_studio_item = DimensionStudioItem.insert(unique_studio_item_id=data['unique_studio_item_id'])
        studio = DimensionStudio.insert(name=data['studio'])
        data_role = DimensionDataRole.insert(role=data['data_role'])
        definition = DimensionDefinition.insert(definition=data['definition'])
        language = DimensionLanguage.insert(iso_code=data['language'])
        audio_channel = DimensionAudioChannels.insert(channel=data['audio_channel'])
        client = DimensionClient.insert(client_id=data['client_id'])
        vendor = DimensionVendor.insert(name=data['vendor'])

        fact = FactServicesAggregatorAggregation.objects.create(
            asset=asset,
            unique_studio_item=unique_studio_item,
            studio=studio,
            file_name=data['file_name'],
            start_time=data['start_time'],
            end_time=data['end_time'],
            file_size=data['file_size'],
            checksum=data['checksum'],
            data_role=data_role,
            content_duration=data['content_duration'],
            definition=definition,
            language=language,
            audio_channel=audio_channel,
            client=client,
            vendor=vendor,
            event_utc_date=DimensionUTCDate.date_from_datetime(datetime=data['event_time']),
            event_utc_datetime=data['event_time']
        )

        return fact
