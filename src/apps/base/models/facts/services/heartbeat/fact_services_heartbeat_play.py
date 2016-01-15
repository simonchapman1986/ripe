from django.db import models
from django_extensions.db.fields import UUIDField

from apps.base.geoip import GEO_IP_LOOKUP

from apps.base.models.dimensions.dimension_client import DimensionClient
from apps.base.models.dimensions.dimension_user import DimensionUser
from apps.base.models.dimensions.dimension_utc_date import DimensionUTCDate
from apps.base.models.dimensions.dimension_play_status import DimensionPlayStatus
from apps.base.models.dimensions.dimension_device import DimensionDevice
from apps.base.models.dimensions.dimension_territory import DimensionTerritory
from apps.base.models.dimensions.dimension_item import DimensionItem

from apps.base.models.facts.services.heartbeat.fact_services_heartbeat_play_buffer import FactServicesHeartbeatPlayBuffer

from apps.base.models.data import get


class FactServicesHeartbeatPlay(models.Model):

    item_id = models.ForeignKey(DimensionItem, default=-1)
    user = models.ForeignKey(DimensionUser, default=-1)
    device = models.ForeignKey(DimensionDevice, default=-1)
    status = models.ForeignKey(DimensionPlayStatus, default=-1)
    country_code = models.ForeignKey(DimensionTerritory, default=-1)
    event_utc_date = models.ForeignKey(DimensionUTCDate, null=True)
    event_time = models.DateTimeField(null=False)
    last_modified = models.DateTimeField(auto_now_add=True, null=True)

    play_buffer = models.ManyToManyField(FactServicesHeartbeatPlayBuffer, default=-1)

    position = models.BigIntegerField(null=True)
    bit_rate = models.BigIntegerField(null=True)

    class Meta:
        app_label = 'base'
        db_table = 'fact_services_heartbeat_plays'

    @classmethod
    def create_fact(cls, **data):

        event_time = data['date']

        # using geoip we assert what our country code is based upon the ip address chain
        country_code = ''
        for ip_address in data['ip_address_chain']:
            country_code = GEO_IP_LOOKUP.get_country_code(ip_address)
            if country_code:
                break

        # lets now fill in our dimensions
        territory = DimensionTerritory.insert(code=country_code)
        client = DimensionClient.insert(client_id=data['client_id'])
        item = DimensionItem.insert(item_id=data['item_id'])
        device = DimensionDevice.insert(item_id=data['device_id'])
        status = DimensionPlayStatus.insert(status=data['status'])
        user = DimensionUser.insert(internal_user_id=data['internal_user_id'],
                                    external_user_id=data['external_user_id'], client=client)

        # we create our fact play object
        fshp = FactServicesHeartbeatPlay.objects.create(
            item_id=item,
            user=user,
            device_id=device,
            status=status,
            event_time=event_time,
            country_code=territory,
            event_utc_date=DimensionUTCDate.date_from_datetime(event_time),
            position=get(data, 'position', disallow=['']),  # Preserve 0
            bit_rate=get(data, 'bitrate', disallow=['']),   # Preserve 0
        )

        # for any occuring buffers we create a play buffer, we can then add this to our many to many relation
        for buffer_duration in get(data, 'buffer_events', disallow=[None, ''], default=[]):
            fshpb = FactServicesHeartbeatPlayBuffer.objects.create(
                duration=buffer_duration,
                event_utc_date=DimensionUTCDate.date_from_datetime(event_time),
                event_time=event_time)

            fshp.play_buffer.add(fshpb)

        # if we have an init in our event - we can add this and add the foreign key to our play event
        # this will make for good and easy lookup of full fact play data
        init_duration = get(data, 'init_length', disallow=[''])
        if init_duration is not None:
            init_licensed = get(data, 'init_licensed', disallow=['', None], default=False)
            FactServicesHeartbeatPlayInit.objects.create(
                heartbeat=fshp,
                duration=init_duration,
                licensed=init_licensed,
                event_utc_date=DimensionUTCDate.date_from_datetime(event_time),
                event_time=event_time)


class FactServicesHeartbeatPlayInit(models.Model):

    heartbeat = models.ForeignKey(FactServicesHeartbeatPlay, default=-1)
    duration = models.BigIntegerField(null=False)
    licensed = models.BooleanField(null=False)
    event_utc_date = models.ForeignKey(DimensionUTCDate, null=True)
    event_time = models.DateTimeField(null=False)
    last_modified = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        app_label = 'base'
        db_table = 'fact_services_heartbeat_play_init'
