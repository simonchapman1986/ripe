from celery.task import task

# main
from apps.base.models import FactServicesBackstageAssetMatch
from apps.base.models import Clients

from apps.cubes.models import CubeAssetMatch

from apps.cubes import aggregator as aggregator

import json


import logging
log = logging.getLogger('reporting')



class AssetMatchCube(aggregator.AggregatorFactory):
    """
    if we wish to override any of the functionality, we can
    examples of methods of override:
        _get_fact() <-- if the fact filter is different than expected - we can alter it here
        _builder() <-- only to be done in extreme circumstance / do we really need to override?

    always check method first before overriding to be clear on your alterations.
    """
    def _sums(self, uuid, row):
        """
        in the event of additional sums we can override this method
        we pass the row as this may well be needed - by default we count
        """
        del self._agg[uuid].__dict__['total_new']

    def _get_fact(self, dim_client, dim_platform):
        """
        we have overridden the _get_fact - as the filter is different on this table
        """

        #orig - produced empty fact always
        # fact = self._fact.objects.filter(
        #     client__client_id=dim_client,
        # )

        #works
        fact = self._fact.objects.filter(
            client__id=dim_client,
        )

        # our basic filter for each aggregate
        self._filter_fact = fact

        # the absolute filter we want internally for computation
        return fact.filter(event_utc_date_id__date=self._date).values(*self._values+('id',))

    def _postconditions(self, key):
        # shallow copy dict (however this copies the iterator - beware)
        dic = self._agg[key].__dict__

        # process used asset ids into json
        row = FactServicesBackstageAssetMatch.objects.get(id=dic['id'])
        used_assets = row.used_asset_ids.all()
        ass = dict()
        for asset in used_assets:
            ass[asset.asset_id] = asset.type

        dic['used_asset_ids'] = json.dumps(ass)

        languages = row.languages.all()
        lang = dict()
        i = 0
        for lan in languages:
            lang[i]=lan.iso_code
            i+=1

        dic['languages_iso_code'] = json.dumps(lang)

        try:
            client = Clients.objects.get(id=dic['client_id'])
            client_name = client.name
        except Clients.DoesNotExist:
            client_name = ''

        dic['client_name'] = client_name

        dic['item_last_modified'] = None

        # now lets give this back
        return self._agg[key].__dict__


@task()
def build_aggregate(date=None):
    b = AssetMatchCube(fact=FactServicesBackstageAssetMatch, agg_fact=CubeAssetMatch, date=date, ignore_platform=True)
    b.set_values(
        *['event_utc_date_id__date',
          'event_utc_date_id__day',
          'event_utc_date_id__month',
          'event_utc_date_id__year',
          'event_utc_date_id__day_of_week',
          'event_utc_date_id__day_name',
          'event_utc_date_id__week_of_year',
          'event_utc_date_id__quarter',
          'client__client_id',
          'item__item_id',
          'item__content_type',
          'item__item_title',
          'item__release_year',
          'item__item_runtime',
          'item__item_duration',
          'item__last_modified',
          'asset__asset_id',
          'asset__type',
          'data_role__role',
          'processing_state__processing_state',
          'provider__provider_id',
          'provider__provider_name',
          'territory__code',
          'spec_name',
          'delivery_date',
          'definition__definition',
          'file_size',
          'duration',
          'id'
        ]
    )

    b.set_map(
        **{
                'event_utc_date_id__date':              'date',
                'event_utc_date_id__day':               'day',
                'event_utc_date_id__month':             'month',
                'event_utc_date_id__year':              'year',
                'event_utc_date_id__day_of_week':       'day_of_week',
                'event_utc_date_id__day_name':          'day_name',
                'event_utc_date_id__week_of_year':      'week_of_year',
                'event_utc_date_id__quarter':           'quarter',
                'client__client_id':                    'client_id',
                'item__item_id':                        'item_id',
                'item__content_type':                   'item_content_type',
                'item__item_title':                     'item_title',
                'item__release_year':                   'item_release_year',
                'item__item_runtime':                   'item_runtime',
                'item__item_duration':                  'item_duration',
                'item__last_modified':                  'item_last_modified',
                'asset__asset_id':                      'asset_id',
                'asset__type':                          'asset_type',
                'data_role__role':                      'data_role',
                'processing_state__processing_state':   'processing_state',
                'provider__provider_id':                'item_provider_id',
                'provider__provider_name':              'item_provider_name',
                'territory__code':                      'territory_code',
                'spec_name':                            'spec_name',
                'delivery_date':                        'delivery_date',
                'definition__definition':               'definition',
                'file_size':                            'file_size',
                'duration':                             'duration',
                'id':                                   'id'
        }
    )

    b.set_unique_values(
        *['id']             # we dont group for this aggregate, we simply process the data
    )

    res, msg = b.build()
    print msg