from celery.task import task

from apps.base.models import FactServicesStorefrontSubscription
from apps.base.models import FactServicesStorefrontTransaction
from apps.base.models import Clients

from apps.cubes.models import CubeSubscriptionRevenueDaily

from apps.cubes import aggregator as aggregator

from decimal import Decimal


class SubscribedRawCube(aggregator.AggregatorFactory):
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
        try:
            tran = FactServicesStorefrontTransaction.objects.filter(
                transaction_id=self._agg[key].__dict__['transaction_id']
            ).latest('event_utc_datetime')
            self._agg[key].__dict__['price'] = Decimal(tran.price)
            self._agg[key].__dict__['card_suffix'] = tran.last_4_digits
        except FactServicesStorefrontTransaction.DoesNotExist:
            self._agg[key].price = Decimal("0.00")
            self._agg[key].__dict__['card_suffix'] = ''

        self._agg[key].__dict__['first_name'] = ''  # we need to acquire this from somewhere? todo
        self._agg[key].__dict__['last_name'] = ''   # we need to acquire this from somewhere? todo

        dic = self._agg[key].__dict__
        try:
            client = Clients.objects.get(id=dic['client_id'])
            client_name = client.name
        except Clients.DoesNotExist:
            client_name = ''

        dic['client_name'] = client_name

        return self._agg[key].__dict__


@task()
def build_aggregate(date=None):
    b = SubscribedRawCube(
        fact=FactServicesStorefrontSubscription,
        agg_fact=CubeSubscriptionRevenueDaily,
        date=date
    )

    b.set_values(
        *[
          'subscription_id',
          'transaction_id',
          'platform_id__os',
          'platform_id__name',
          'platform_id__version',
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
          'subscription_status_id__description',
        ]
    )

    b.set_map(
        **{
            'user_id__territory_id__code':          'territory_code',
            'user_id__client_id__client_id':        'client_id',
            'subscription_status_id__description':  'subscription_status',
            'event_utc_date_id__date':              'date',
            'event_utc_date_id__year':              'year',
            'event_utc_date_id__month':             'month',
            'event_utc_date_id__day':               'day',
            'event_utc_date_id__day_of_week':       'day_of_week',
            'event_utc_date_id__day_name':          'day_name',
            'event_utc_date_id__week_of_year':      'week_of_year',
            'event_utc_date_id__quarter':           'quarter',
            'platform_id__os':                      'os',
            'platform_id__name':                    'name',
            'platform_id__version':                 'version',
            'transaction_id':                       'transaction_id',
        }
    )

    b.set_unique_values(
        *['id']
    )

    res, msg = b.build()
    print msg
