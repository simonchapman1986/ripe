from celery.task import task

from apps.cubes.models.daily.plays_by_item import CubePlaysByItem
from apps.base.models.facts.services.heartbeat.fact_services_heartbeat_play import FactServicesHeartbeatPlay
from apps.base.models.facts.services.backstage.fact_services_backstage_item_metadata import FactServicesBackstageItemMetadata
from apps.base.models.dimensions.dimension_client import DimensionClient
from apps.cubes import aggregator as aggregator

class PlaysByItemCube(aggregator.AggregatorFactory):
    """
    if we wish to override any of the functionality, we can
    examples of methods of override:
        _get_fact() <-- if the fact filter is different than expected - we can alter it here
        _builder() <-- only to be done in extreme circumstance / do we really need to override?

    always check method first before overriding to be clear on your alterations.
    """
    def _get_fact(self, dim_client, dim_platform):
        """
        we have overridden the _get_fact - as the filter is different on this table
        """
        fact = self._fact.objects.filter(
            user_id__client_id__client_id=dim_client,
            event_utc_date_id__date=self._date,
        ).values(*self._values)

        return fact

    def _sums(self, uuid, row):
        """
        sum aggregates for our table - we have extras that we need to specify for
        our cube - these are related to the total revenue for each
        """
        self._agg[uuid].total_new += 1
        self._agg[uuid].total = 0

    def _preconditions(self, row=dict):
        try:
            self.meta = FactServicesBackstageItemMetadata.objects.get(item_meta__item_id=row['item_id__item_id'])
            row['metadata_id'] = self.meta.metadata_id
        except FactServicesBackstageItemMetadata.DoesNotExist:
            # No Metadata for Item
            pass

        return row, True

    def _postconditions(self, key):
        try:
            self._agg[key].__dict__['metadata_id'] = self.meta.metadata_id
            self._agg[key].__dict__['item_title'] = self.meta.title
            self._agg[key].__dict__['item_provider_name'] = self.meta.provider_name
            self._agg[key].__dict__['item_isan'] = self.meta.isan
            self._agg[key].__dict__['item_eidr'] = self.meta.eidr
            self._agg[key].__dict__['item_genres'] = self.meta.genres
            self._agg[key].__dict__['item_release_date'] = self.meta.release_date
            self._agg[key].__dict__['item_release_date'] = self.meta.release_date
            self._agg[key].__dict__['item_production_company'] = self.meta.production_company
            self._agg[key].__dict__['item_release_year'] = self.meta.release_year
            self._agg[key].__dict__['item_primary_language'] = self.meta.primary_language.iso_code
            self._agg[key].__dict__['item_runtime'] = self.meta.runtime
            self._agg[key].__dict__['item_vendor_name'] = self.meta.vendor.name
            self._agg[key].__dict__['item_episode_number'] = self.meta.episode_number
            self._agg[key].__dict__['item_season'] = self.meta.season
            self._agg[key].__dict__['item_show_title'] = self.meta.show_title
            self._agg[key].__dict__['item_ultraviolet'] = self.meta.ultraviolet
        except:
            # Metadata missing
            pass


        # calculate total
        dic = self._agg[key].__dict__

        # remove date attributes as we dont want to filter this... + a couple others
        date_params = [
            'date',
            'year',
            'month',
            'day',
            'day_of_week',
            'day_name',
            'week_of_year',
            'quarter',
            'total_new',
            'average_per_day',
            'breakdown_pct',
            'change',
            'total',
            ]

        # we are going to store these values for a short period
        temp_store = {}

        # we will now iterate over our params and temp store it, then delete it.
        for k in date_params:
            temp_store[k] = self._agg[key].__dict__[k]
            del dic[k]

        agg = self._agg_fact
        res = agg.objects.filter(**dic).exclude(date__gt=self._date_obj)

        t = 0
        for r in res:
            t+=r.total_new

        total = t+dic['total_new']

        # we can now re-insert our params we took out so we can store our data
        for k in date_params:
            self._agg[key].__dict__[k] = temp_store[k]

        self._agg[key].total = total

        return self._agg[key].__dict__

    @property
    def _get_clients(self):
        return [a.client_id for a in DimensionClient.objects.all()]


@task()
def build_aggregate(date=None):
    b = PlaysByItemCube(fact=FactServicesHeartbeatPlay, agg_fact=CubePlaysByItem, date=date, ignore_platform=True)
    b.set_values(
        *['item_id',
          'status',
          'event_utc_date_id__date',
          'event_utc_date_id__day',
          'event_utc_date_id__month',
          'event_utc_date_id__year',
          'event_utc_date_id__day_of_week',
          'event_utc_date_id__day_name',
          'event_utc_date_id__week_of_year',
          'event_utc_date_id__quarter',
          'device_id',
          'user_id__client_id__client_id',
          'user_id__territory_id__code']
    )

    b.set_map(
        **{
            'item_id':                               'item_id',
            'status':                                'status',
            'event_utc_date_id__date':               'date',
            'event_utc_date_id__year':               'year',
            'event_utc_date_id__month':              'month',
            'event_utc_date_id__day':                'day',
            'event_utc_date_id__day_of_week':        'day_of_week',
            'event_utc_date_id__day_name':           'day_name',
            'event_utc_date_id__week_of_year':       'week_of_year',
            'event_utc_date_id__quarter':            'quarter',
            'device_id':                             'device_id',
            'user_id__client_id__client_id':         'client_id',
            'user_id__territory_id__code':           'territory_code',
        }
    )

    b.set_unique_values(
        *['item_id',
          'status',
          'device_id',
          'user_id__client_id__client_id',
          'user_id__territory_id__code',
          'event_utc_date_id__date',
          'metadata_id']
    )

    res, msg = b.build()
    print msg
