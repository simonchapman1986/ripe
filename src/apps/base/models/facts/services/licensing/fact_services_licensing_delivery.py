from django.db import models
from django_extensions.db.fields import UUIDField
from apps.base.models.data import get
from apps.base.models.dimensions.dimension_client import DimensionClient
from apps.base.models.dimensions.dimension_device import DimensionDevice
from apps.base.models.dimensions.dimension_user import DimensionUser
from apps.base.models.dimensions.dimension_utc_date import DimensionUTCDate


class FactServicesLicensingDelivery(models.Model):

    user = models.ForeignKey(DimensionUser, default=-1)
    device = models.ForeignKey(DimensionDevice, default=-1)
    drm_type = models.CharField(max_length=255)
    event_utc_datetime = models.DateTimeField()
    event_utc_date = models.ForeignKey(DimensionUTCDate, null=True)
    transaction_id = UUIDField(version=4)

    class Meta:
        app_label = 'base'
        db_table = 'fact_services_licensing_delivery'

    @classmethod
    def create_fact(cls, data):
        # This is a DRM Device Id, not a Device Id.
        device, _ = DimensionDevice.objects.get_or_create(device_id=data['device_id'])
        client = DimensionClient.insert(client_id=data['client_id'])

        external_user_id = get(data, 'external_user_id', default=None)
        if external_user_id:
            user = DimensionUser.insert(external_user_id=external_user_id, client=client)
        else:
            user = DimensionUser.objects.get(id=-1)

        cls.objects.create(
            device=device,
            drm_type=data['drm_type'],
            user=user,
            transaction_id=data.get('transaction_id', None),
            event_utc_datetime=data['event_time'],
            event_utc_date=DimensionUTCDate.date_from_datetime(data['event_time']),
        )
