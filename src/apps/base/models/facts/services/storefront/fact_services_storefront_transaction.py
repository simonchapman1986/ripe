from django.db import models
from django_extensions.db.fields import UUIDField
from apps.base.models.data import get
from apps.base.models.dimensions.dimension_client import DimensionClient
from apps.base.models.dimensions.dimension_device import DimensionDevice
from apps.base.models.dimensions.dimension_platform import DimensionPlatform
from apps.base.models.dimensions.dimension_territory import DimensionTerritory
from apps.base.models.dimensions.dimension_user import DimensionUser
from apps.base.models.dimensions.dimension_item import DimensionItem
from apps.base.models.dimensions.dimension_product import DimensionProduct
from apps.base.models.dimensions.dimension_window import DimensionWindow
from apps.base.models.dimensions.dimension_account import DimensionAccount
from apps.base.models.dimensions.dimension_right import DimensionRight
from apps.base.models.dimensions.dimension_retail_model import DimensionRetailModel
from apps.base.models.dimensions.dimension_definition import DimensionDefinition
from apps.base.models.dimensions.dimension_currency import DimensionCurrency
from apps.base.models.dimensions.dimension_store_transaction_status import DimensionStoreTransactionStatus
from apps.base.models.dimensions.dimension_utc_date import DimensionUTCDate
from django.utils import timezone
from apps.base.models.facts.services.storefront.tools.fact_tools import exists
from apps.base.models.facts.services.storefront.tools.fact_tools import save_user
from apps.base.models.facts.services.storefront.tools.fact_tools import save_platform

import logging
log = logging.getLogger('reporting')

class FactServicesStorefrontTransaction(models.Model):

    item = models.ForeignKey(DimensionItem, null=True)
    product = models.ForeignKey(DimensionProduct, null=True)
    window = models.ForeignKey(DimensionWindow, null=True)
    transaction_id = models.CharField(max_length=255, null=True, default=None)
    transaction_status = models.ForeignKey(DimensionStoreTransactionStatus, null=True)
    user = models.ForeignKey(DimensionUser, null=True)
    account = models.ForeignKey(DimensionAccount, null=True)
    right = models.ForeignKey(DimensionRight, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    currency = models.ForeignKey(DimensionCurrency, null=True)
    retail_model = models.ForeignKey(DimensionRetailModel, null=True)
    definition = models.ForeignKey(DimensionDefinition, null=True)
    client = models.ForeignKey(DimensionClient, null=True)
    territory = models.ForeignKey(DimensionTerritory, null=True)
    platform = models.ForeignKey(DimensionPlatform, null=True)
    device = models.ForeignKey(DimensionDevice, null=True)
    mnc = models.CharField(max_length=255, null=True)
    mcc = models.CharField(max_length=255, null=True)
    last_4_digits = models.CharField(max_length=4, null=True, default='')

    event_utc_datetime = models.DateTimeField(null=True)
    event_utc_date = models.ForeignKey(DimensionUTCDate, null=True)
    last_modified_utc = models.DateTimeField(auto_now_add=True, auto_now=True)

    class Meta:
        app_label = 'base'
        db_table = 'fact_services_storefront_transaction'

    @classmethod
    def create_fact(cls, logs, **data):

        # insert dims
        item = DimensionItem.insert(item_id=data.get('item_id')) if exists('item_id', data) else None
        product = DimensionProduct.insert(product_id=data.get('product_id')) if exists('product_id', data) else None
        right = DimensionRight.insert(right_id=data.get('right_id')) if exists('right_id', data) else None
        currency = DimensionCurrency.insert(code=data.get('currency')) if exists('currency', data) else None
        retail_model = DimensionRetailModel.insert(
            model=data.get('retail_model')
        ) if exists('retail_model', data) else None
        definition = DimensionDefinition.insert(
            definition=data.get('definition')
        ) if exists('definition', data) else None

        window = DimensionWindow.insert(
            window_id=data.get('window_id', None),
            product=product,
            usage_right=right,
            item=item
        )
        transaction_status = DimensionStoreTransactionStatus.insert(
            status=data.get('transaction_status')
        ) if exists('transaction_status', data) else None

        platform = save_platform(data, event='Storefront Transaction')

        territory = DimensionTerritory.insert(code=data.get('territory')) if exists('territory', data) else None
        client = DimensionClient.insert(client_id=data.get('client_id')) if exists('client_id', data) else None

        user = save_user(data, territory, client, event='Storefront Transaction')

        account = DimensionAccount.insert(
            account_id=data.get(
                'account_id', data.get(
                    'external_user_id', data.get(
                        'internal_user_id', None
                    )
                )
            )
        )

        try:
            device = DimensionDevice.insert(
                make=data.get('make', ''),
                model=data.get('model', ''),
                os=data.get('os', ''),
                os_version=data.get('version', ''),
            )if any([
                d in data for d in ['make', 'model', 'os', 'version']
            ]) else None
        except:
            log.exception('')

        try:
            trans = cls.objects.get(transaction_id=data.get('transaction_id', ''))
            trans.last_4_digits = data.get('last_4_digits', None)
            trans.event_utc_datetime = data.get('event_time', timezone.now().isoformat())
            trans.event_utc_date = DimensionUTCDate.date_from_datetime(data.get('event_time', timezone.now().isoformat()))
            trans.save()
        except cls.DoesNotExist as e:
            trans = cls.objects.create(
                item=item,
                product=product,
                window=window,
                transaction_id=data.get('transaction_id', None),
                transaction_status=transaction_status,
                user=user,
                account=account,
                right=right,
                price=data.get('price', 0.00),
                currency=currency,
                retail_model=retail_model,
                definition=definition,
                client=client,
                territory=territory,
                platform=platform,
                device=device,
                mnc=data.get('MNC', None),
                mcc=data.get('MCC', None),
                last_4_digits=data.get('last_4_digits', None),
                event_utc_datetime=data.get('event_time', timezone.now().isoformat()),
                event_utc_date=DimensionUTCDate.date_from_datetime(data.get('event_time', timezone.now().isoformat())),
            )

        try:
            cls.objects.get(pk=trans.pk)
            exist = True
        except cls.DoesNotExist:
            exist = False

        logs.completed = exist
        logs.save()
