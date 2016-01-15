from django.db import models
from django_extensions.db.fields import UUIDField
from apps.base.models.data import get
from apps.base.models.dimensions.dimension_client import DimensionClient
from apps.base.models.dimensions.dimension_device import DimensionDevice
from apps.base.models.dimensions.dimension_user import DimensionUser
from apps.base.models.dimensions.dimension_item import DimensionItem
from apps.base.models.dimensions.dimension_utc_date import DimensionUTCDate


class FactServicesStorefrontDownload(models.Model):

    item = models.ForeignKey(DimensionItem, default=-1)
    user = models.ForeignKey(DimensionUser, default=-1)
    device = models.ForeignKey(DimensionDevice, default=-1)
    product_id = UUIDField(version=4)
    asset_id = UUIDField(version=4)
    status = models.CharField(max_length=255)
    network = models.CharField(max_length=255, null=True)
    expiry_date = models.DateTimeField(null=False)

    event_utc_datetime = models.DateTimeField()
    event_utc_date = models.ForeignKey(DimensionUTCDate, null=True)
    last_modified_utc = models.DateTimeField(auto_now_add=True, auto_now=True)

    class Meta:
        app_label = 'base'
        db_table = 'fact_services_storefront_download'

    @classmethod
    def create_fact(cls, **data):
        item = DimensionItem.insert(item_id=data['item_id'])
        device, _ = DimensionDevice.objects.get_or_create(device_id=data['device_id'])
        client = DimensionClient.insert(client_id=data['client_id'])

        external_user_id = get(data, 'external_user_id', default='')
        internal_user_id = get(data, 'internal_user_id', default='')
        user = DimensionUser.insert(
            external_user_id=external_user_id,
            internal_user_id=internal_user_id,
            client=client
        )

        # store the fact
        cls.objects.create(
            item=item,
            user=user,
            device=device,
            product_id=data['product_id'],
            asset_id=data['asset_id'],
            status=data['status'],
            network=data['network'],
            expiry_date=data['expiry_date'],
            event_utc_datetime=data['event_time'],
            event_utc_date=DimensionUTCDate.date_from_datetime(data['event_time']),
        )

