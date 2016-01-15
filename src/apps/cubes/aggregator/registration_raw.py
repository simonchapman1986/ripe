
from celery.task import task

from apps.base.models import FactServicesStorefrontRegistration
from apps.base.models import Clients

from apps.cubes.models import CubeRegistrationRawDaily

from apps.cubes import aggregator as aggregator

import logging
log = logging.getLogger('reporting')

import gc


class RegistrationsRawCube(aggregator.AggregatorFactory):
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
            client = Clients.objects.get(id=self._agg[key].__dict__['client_id'])
            client_name = client.name
        except Clients.DoesNotExist:
            client_name = ''

        self._agg[key].__dict__['client_name'] = client_name

        return self._agg[key].__dict__


@task()
def build_aggregate(date=None):
    b = RegistrationsRawCube(
        fact=FactServicesStorefrontRegistration,
        agg_fact=CubeRegistrationRawDaily,
        date=date
    )

    b.set_values(
        *[
            'user_id__client_id__client_id',
            'user_id__internal_user_id',
            'user_id__external_user_id',
            'user_id__first_name',
            'user_id__last_name',
            'event_utc_date_id__date',
            'event_utc_date_id__day',
            'event_utc_date_id__month',
            'event_utc_date_id__year',
            'event_utc_date_id__day_of_week',
            'event_utc_date_id__day_name',
            'event_utc_date_id__week_of_year',
            'event_utc_date_id__quarter',
            'user_id__territory_id__code'
        ]
    )

    b.set_map(
        **{
            'user_id__client_id__client_id':        'client_id',
            'user_id__internal_user_id':            'internal_user_id',
            'user_id__external_user_id':            'external_user_id',
            'event_utc_date_id__date':              'date',
            'event_utc_date_id__year':              'year',
            'event_utc_date_id__month':             'month',
            'event_utc_date_id__day':               'day',
            'event_utc_date_id__day_of_week':       'day_of_week',
            'event_utc_date_id__day_name':          'day_name',
            'event_utc_date_id__week_of_year':      'week_of_year',
            'event_utc_date_id__quarter':           'quarter',
            'user_id__first_name':                  'first_name',
            'user_id__last_name':                   'last_name',
            'user_id__territory_id__code':          'territory_code',
        }
    )

    b.set_unique_values(
        *['id']
    )

    res, msg = b.build()
    del b
    gc.collect()
    print msg
