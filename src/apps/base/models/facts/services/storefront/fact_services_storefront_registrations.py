from django.db import models

from tools.platform import get_platform

from apps.base.models.dimensions.dimension_client import DimensionClient
from apps.base.models.dimensions.dimension_platform import DimensionPlatform
from apps.base.models.dimensions.dimension_user import DimensionUser
from apps.base.models.dimensions.dimension_device import DimensionDevice
from apps.base.models.dimensions.dimension_utc_date import DimensionUTCDate
from apps.base.models.dimensions.dimension_territory import DimensionTerritory
from apps.base.models.dimensions.dimension_account import DimensionAccount


import logging
log = logging.getLogger('reporting')


class FactServicesStorefrontRegistration(models.Model):
    account = models.ForeignKey(DimensionAccount, default=-1)
    user = models.ForeignKey(DimensionUser)
    client = models.ForeignKey(DimensionClient)
    platform = models.ForeignKey(DimensionPlatform, default=-1)
    device = models.ForeignKey(DimensionDevice, default=-1)
    mnc = models.CharField(max_length=255, null=True)
    mcc = models.CharField(max_length=255, null=True)

    event_utc_date = models.ForeignKey(DimensionUTCDate)
    event_utc_datetime = models.DateTimeField()
    last_modified_utc = models.DateTimeField(auto_now_add=True, auto_now=True)

    class Meta:
        app_label = 'base'
        db_table = 'fact_services_storefront_registrations'

    @classmethod
    def create_fact(cls, logs, **data):

        platform = get_platform(local_data=data, model=FactServicesStorefrontRegistration)
        territory = DimensionTerritory.insert(code=data['territory'])
        client = DimensionClient.insert(client_id=data['client_id'])
        try:
            device = DimensionDevice.insert(
                device_id=data.get('device_id', ''),
                make=data.get('make', ''),
                model=data.get('model', ''),
                os=data.get('os', ''),
                os_version=data.get('version', '')
            )
        except:
            device = None

        try:
            user_info = data.get('attributes', None)
            user = DimensionUser.insert(
                internal_user_id=data.get('internal_user_id', data.get('user_id', '')),
                external_user_id=data.get('external_user_id', ''),
                territory=territory,
                client=client,
                email=data.get('email', None),
                first_name=user_info.get('first_name', '') if user_info else '',
                last_name=user_info.get('last_name', '') if user_info else '',
                marketing_preference=user_info.get('marketing_preference', '') if user_info else '',
                country_of_residence=user_info.get('country_of_residence', '') if user_info else None
            )
        except Exception:
            user = None

        try:
            account = DimensionAccount.insert(
                account_id=data.get('external_user_id', data.get('internal_user_id', '')),
                account_created=data.get('account_created', None)
            )
        except:
            account = None

        fact = FactServicesStorefrontRegistration.objects.create(
            account=account,
            user=user,
            client=client,
            platform=platform,
            device=device,
            event_utc_date=DimensionUTCDate.date_from_datetime(datetime=data['event_time']),
            event_utc_datetime=data['event_time'],
            mnc=data.get('MNC', None),
            mcc=data.get('MCC', None)
        )

        try:
            FactServicesStorefrontRegistration.objects.get(pk=fact.pk)
            exist = True
        except FactServicesStorefrontRegistration.DoesNotExist:
            exist = False

        logs.completed = exist
        logs.save()
