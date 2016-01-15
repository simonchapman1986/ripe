from celery.task import task

from apps.base.models import FactServicesLicensingDelivery
from apps.base.models import FactServicesStorefrontTransaction
from apps.base.models import FactServicesBackstageItemMetadata
from apps.base.models import Clients

from apps.cubes.models import CubeLicenseDeliveryRawDaily
from apps.cubes import aggregator as aggregator


class DeliveryRawCube(aggregator.AggregatorFactory):
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

    def _preconditions(self, row=dict):
        return row, True

    def _postconditions(self, key):

        tran_id = self._agg[key].__dict__['transaction_id']
        item_id = self._agg[key].__dict__['item_id']
        try:
            tran = FactServicesStorefrontTransaction.objects.filter(transaction_id=tran_id).latest('event_utc_datetime')
            self._agg[key].__dict__['platform_name'] = tran.platform.name
        except FactServicesStorefrontTransaction.DoesNotExist:
            self._agg[key].__dict__['platform_name'] = ''

        try:
            item = FactServicesBackstageItemMetadata.objects.filter(item_id=item_id).latest('event_utc_datetime')
            self._agg[key].__dict__['item_id'] = item.item_meta.item_id
            self._agg[key].__dict__['item_title'] = item.item_meta.item_title
        except FactServicesBackstageItemMetadata.DoesNotExist:
            self._agg[key].__dict__['item_id'] = ''
            self._agg[key].__dict__['item_title'] = ''

        try:
            client = Clients.objects.get(id=self._agg[key].__dict__['client_id'])
            client_name = client.name
        except Clients.DoesNotExist:
            client_name = ''

        self._agg[key].__dict__['client_name'] = client_name


        return self._agg[key].__dict__


@task()
def build_aggregate(date=None):
    b = DeliveryRawCube(
        fact=FactServicesLicensingDelivery,
        agg_fact=CubeLicenseDeliveryRawDaily,
        date=date
    )

    b.set_values(
        *[
          'transaction_id',
          'event_utc_date_id__date',
          'event_utc_date_id__day',
          'event_utc_date_id__month',
          'event_utc_date_id__year',
          'event_utc_date_id__day_of_week',
          'event_utc_date_id__day_name',
          'event_utc_date_id__week_of_year',
          'event_utc_date_id__quarter',
          'user_id__client_id__client_id',
          'user_id__territory_id__code',
          'device_id__device_id',
          'device_id__make',
          'device_id__model',
          'device_id__os',
          'device_id__os_version',
          'drm_type',
        ]
    )

    b.set_map(
        **{
            'user_id__territory_id__code':          'territory_code',
            'user_id__client_id__client_id':        'client_id',
            'event_utc_date_id__date':              'date',
            'event_utc_date_id__year':              'year',
            'event_utc_date_id__month':             'month',
            'event_utc_date_id__day':               'day',
            'event_utc_date_id__day_of_week':       'day_of_week',
            'event_utc_date_id__day_name':          'day_name',
            'event_utc_date_id__week_of_year':      'week_of_year',
            'event_utc_date_id__quarter':           'quarter',
            'transaction_id':                       'transaction_id',
            'device_id__device_id':                 'device_id',
            'device_id__make':                      'device_make',
            'device_id__model':                     'device_model',
            'device_id__os':                        'device_os',
            'device_id__os_version':                'device_os_version',
            'drm_type':                             'drm_type',
        }
    )

    b.set_unique_values(
        *['id']
    )

    res, msg = b.build()
    print msg
