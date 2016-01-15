from django.db import models
from apps.base.models.dimensions.dimension_client import DimensionClient
from apps.base.models.dimensions.dimension_item import DimensionItem
from apps.base.models.dimensions.dimension_assets import DimensionAssets
from apps.base.models.dimensions.dimension_item_provider import DimensionItemProvider
from apps.base.models.dimensions.dimension_utc_date import DimensionUTCDate
from apps.base.models.dimensions.dimension_language import DimensionLanguage
from apps.base.models.dimensions.dimension_data_role import DimensionDataRole
from apps.base.models.dimensions.dimension_processing_state import DimensionProcessingState
from apps.base.models.dimensions.dimension_territory import DimensionTerritory
from apps.base.models.dimensions.dimension_definition import DimensionDefinition
from apps.base.models.utilities.client import Clients
import datetime
from django.conf import settings

import logging
log = logging.getLogger('reporting')
trace = logging.getLogger('trace')


class FactServicesBackstageAssetMatch(models.Model):

    client = models.ForeignKey(DimensionClient, related_name='matched_client')
    item = models.ForeignKey(DimensionItem, related_name='matched_item')
    asset = models.ForeignKey(DimensionAssets, default=-1, related_name='matched_asset')
    data_role = models.ForeignKey(DimensionDataRole)
    processing_state = models.ForeignKey(DimensionProcessingState)
    used_asset_ids = models.ManyToManyField(DimensionAssets)
    provider = models.ForeignKey(DimensionItemProvider, related_name='matched_provider')
    territory = models.ForeignKey(DimensionTerritory)
    spec_name = models.CharField(max_length=128, null=True, blank=True)
    delivery_date = models.DateTimeField(default=None)
    definition = models.ForeignKey(DimensionDefinition, null=True, blank=True)
    languages = models.ManyToManyField(DimensionLanguage)  # models.CharField(max_length=256, null=True, blank=True)
    file_size = models.BigIntegerField(max_length=10)
    duration = models.IntegerField(max_length=10, default='')
    event_date = models.DateField(default=None)
    event_utc_date = models.ForeignKey(DimensionUTCDate)
    event_utc_datetime = models.DateTimeField(default=None)
    last_modified_utc = models.DateTimeField(auto_now_add=True, auto_now=True)

    class Meta:
        app_label = 'base'
        db_table = 'fact_services_backstage_asset_match'

    @classmethod
    def create_fact(cls, **data):
        client = DimensionClient.insert(client_id=data['client_id'])
        item = DimensionItem.insert(item_id=data['item_id'])
        data_role = DimensionDataRole.insert(role=data['data_role'])

        definition = DimensionDefinition.insert(definition=data['definition'])

        processing_state = DimensionProcessingState.insert(processing_state=data['processing_state'])
        territory = DimensionTerritory.insert(code=data['territory'])

        asset = DimensionAssets.insert(
            asset_id=data['asset_id'],
            type=data['asset_type']
        )

        provider = DimensionItemProvider.insert(
            True,
            provider_id=data['provider_item_id'],
            provider_name=data['provider'],
            )


        delivery_date = datetime.datetime.strptime(str(data['delivery_date']), settings.DATETIME_FORMAT)
        event_date = datetime.datetime.strptime(data['event_time'], settings.DATETIME_FORMAT)
        event_utc_datetime = datetime.datetime.strptime(data['event_time'], settings.DATETIME_FORMAT)

        fact = FactServicesBackstageAssetMatch.objects.create(
            client=client,
            item=item,
            asset=asset,
            data_role=data_role,
            processing_state=processing_state,
            provider=provider,
            territory=territory,
            spec_name=data['spec_name'],
            delivery_date=delivery_date,
            definition=definition,
            file_size=data['file_size'],
            duration=data['duration'],
            event_date=event_date.date(),
            event_utc_date=DimensionUTCDate.date_from_datetime(datetime=data['event_time']),
            event_utc_datetime=event_utc_datetime
        )

        fact.save()
        if data['used_asset_ids']:
            for asset_id in data['used_asset_ids']:
                asset_dim = DimensionAssets.objects.get_or_create(asset_id=asset_id)
                fact.used_asset_ids.add(asset_dim[0].id)
        else:
            fact.used_asset_ids = ''

        if data['languages']:
            for language in data['languages']:
                lang_dim = DimensionLanguage.objects.get_or_create(iso_code=language)
                fact.languages.add(lang_dim[0].id)
        else:
            fact.languages = ''
        return fact

    @classmethod
    def get_data(cls,  start, end, filters=None, group=None):

        cls.filter_content_data(start, end, filters=filters)

        if not len(cls.data):
            log.debug('NO CONTENT DATA AVAILABLE FOR GIVEN FILTERS. start-date: {} end-date: {}'.format(
                start.strftime(settings.DATE_FORMAT_YMD), end.strftime(settings.DATE_FORMAT_YMD))
            )
            return None

        d = cls.data.values()

        csv_fields = {
            'client_id': 'client',
            'asset_id': 'asset_id',
            'asset_type': 'asset_type',
            'data_role_id': 'data_role',
            'territory_id': 'territory',
            'processing_state_id': 'processing_state',
            'definition_id': 'definition'
        }
        reslist = list()
        for rec in d:
            used_asset_id_vals = cls.get_used_asset_ids(rec)
            asset_languages = cls.get_asset_lanugages(rec)
            rec.update({
                'asset_type': rec['asset_id'],
                'item_title': rec['item_id'],
                'provider_name': rec['provider_id']
            })
            csv_rec = dict()
            for k, v in rec.iteritems():
                val = cls.get_name_for_field(k, rec)
                csv_rec[
                    csv_fields[k] if k in csv_fields else k
                ] = str(val) if not isinstance(val, datetime.datetime) else val
            csv_rec['languages'] = asset_languages
            csv_rec['used_asset_ids'] = used_asset_id_vals
            csv_rec['delivery_date'] = csv_rec['delivery_date'].date().strftime(settings.DATE_FORMAT_YMD)
            csv_rec['territory'] = csv_rec['territory'].upper()
            csv_rec['definition'] = csv_rec['definition'].upper()
            reslist.append(csv_rec)
        return reslist



    @classmethod
    def get_name_for_field(cls, k, rec):
        dims = {
            'client_id': (DimensionClient, 'client_id'),
            'item_id': (DimensionItem, 'item_id'),
            'item_title': (DimensionItem, 'item_title'),
            'asset_id': (DimensionAssets, 'asset_id'),
            'asset_type': (DimensionAssets, 'type'),
            'provider_id': (DimensionItemProvider, 'provider_id'),
            'provider_name': (DimensionItemProvider, 'provider_name'),
            'data_role_id': (DimensionDataRole, 'role'),
            'processing_state_id': (DimensionProcessingState, 'processing_state'),
            'definition_id': (DimensionDefinition, 'definition'),
            'territory_id': (DimensionTerritory, 'code')

        }

        try:
            field_id = getattr(dims[k][0].objects.get(id=rec[k]), dims[k][1]) if k in dims else rec[k]
            if k == 'client_id':
                client_name = Clients.objects.get(id=field_id).name
                client_name = field_id if not client_name else client_name
            excp = ['client_id', 'delivery_date']
            if k not in excp:
                if k == 'definition':
                    field_id = str(field_id).upper()
                else:
                    field_id = str(field_id).title()
            return client_name if k == 'client_id' else field_id

        except Exception as e:
            return field_id if k == 'client_id' else rec[k]


    @classmethod
    def filter_content_data(cls, start, end, filters=None):
        cls.data = FactServicesBackstageAssetMatch.objects.all()
        cls.data = cls.data.filter(event_date__gte=start).filter(event_date__lte=end)
        if isinstance(filters, dict):
            if len(cls.data) and len(filters):
                keys = filters.keys()
                if 'client_id' in keys:
                    cls.data = cls.data.filter(client_id=filters['client_id'])


    @classmethod
    def get_used_asset_ids(cls, rec):
        used_asset_id_vals = ''
        r = cls.data.get(id=rec['id'])
        asset_ids_used = r.used_asset_ids.all()
        if len(asset_ids_used):
            used_asset_ids_list = list()
            for i in asset_ids_used:
                used_asset_ids_list.append(i.asset_id)
            used_asset_id_vals = ','.join([x for x in used_asset_ids_list])
        return used_asset_id_vals

    @classmethod
    def get_asset_lanugages(cls, rec):
        asset_languages_vals = ''
        r = cls.data.get(id=rec['id'])
        asset_languages = r.languages.all()
        if len(asset_languages):
            asset_language_list = list()
            for i in asset_languages:
                asset_language_list.append(i.iso_code)
            asset_languages_vals = ','.join([str(x).title() for x in asset_language_list])
        return asset_languages_vals



def check():
    """
    >>> check()
    >>> 1
    """
    data = {
        "asset_id": "e19088f0-8709-4607-8f7e-1839f6bf5780",
        "definition": "HD",
        "processing_state": "raw",
        "duration": "3440",
        "file_size": "16050803086",
        "languages": ["eng", "fre"],
        "provider_item_id": "01800A",
        "spec_name": "Paramount 5.1 WAV",
        "client_id": "098b3600-e6b5-4ce9-8295-1e21d77b9132",
        "provider": "Paramount",
        "item_id": "76fc452b-e458-49ef-a5d4-0f162a0122c6",
        "event_time": "2010-01-01 02:21:11",
        "data_role": "feature",
        "territory": "GB",
        "asset_type": "audio",
        "delivery_date": "2010-01-01 01:58:11",
        "used_asset_ids": ['e19088f0-8709-4607-8f7e-1839f6bf5781', 'e19088f0-8709-4697-8f7e-1839f6bf5780']
    }
    FactServicesBackstageAssetMatch.create_fact(**data)
    # from datetime import datetime
    # st_date = end_date = "2010-01-01"
    # start = datetime.strptime(st_date, DATE_FORMAT)
    # end = datetime.strptime(end_date, DATE_FORMAT)
    # res = FactServicesBackstageAssetMatch.get_data(start, end)
    # for r in res:
    #     print r.id, r.client_id, r.item_id, r.asset_id, r.data_role_id, r.spec_name, r.delivery_date
    # print res


