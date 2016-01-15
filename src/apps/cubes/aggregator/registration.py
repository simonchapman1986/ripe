from celery.task import task

from apps.base.models import FactServicesStorefrontRegistration
from apps.base.models import Clients

from apps.cubes.models import CubeRegistrationsDaily

from apps.cubes import aggregator as aggregator
import gc
import logging
log = logging.getLogger('reporting')


class RegisteredUsersCube(aggregator.AggregatorFactory):
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
        self._agg[uuid].total_new += 1
        self._agg[uuid].average_per_day = 0
        self._agg[uuid].breakdown_pct = 0
        self._agg[uuid].change = 0
        self._agg[uuid].total = 0

    def _postconditions(self, key):
        # shallow copy dict (however this copies the iterator - beware)
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

        # if we have no average, our average will equal that of the total new
        p_avg = dic['total_new']

        # we will now iterate over our params and temp store it, then delete it.
        for k in date_params:
            temp_store[k] = self._agg[key].__dict__[k]
            del dic[k]

        # shallow copy our agg then query with our amended filters
        agg = self._agg_fact
        res = agg.objects.filter(**dic).exclude(date__gt=self._date_obj)

        # we are now going to sum up our total new
        t = 0
        last = 0
        for r in res:
            t+=r.total_new
            last = r.total

        total = t+p_avg

        try:
            # with this we should be able to give an average, obviously this will fail if 0, so we catch this
            # and then default to our original total
            avg = total / len(res)
        except Exception:
            avg = p_avg

        # we can now re-insert our params we took out so we can store our data
        for k in date_params:
            self._agg[key].__dict__[k] = temp_store[k]

        # as we had a few certain params in the temp store, we can only now override with the ones we have generated
        self._agg[key].average_per_day = avg
        self._agg[key].breakdown_pct = 0
        self._agg[key].total = total

        # we give a churn here..
        try:
            self._agg[key].change = total - last
        except:
            self._agg[key].change = 0

        try:
            client = Clients.objects.get(id=self._agg[key].__dict__['client_id'])
            client_name = client.name
        except Clients.DoesNotExist:
            client_name = ''
        self._agg[key].__dict__['client_name'] = client_name


        # now lets give this back
        return self._agg[key].__dict__


@task()
def build_aggregate(date=None):

    b = RegisteredUsersCube(
        fact=FactServicesStorefrontRegistration,
        agg_fact=CubeRegistrationsDaily,
        date=date
    )

    b.set_values(
        *['client_id__client_id',
          'platform_id__os',
          'platform_id__name',
          'platform_id__version',
          'device__make',
          'device__model',
          'device__os',
          'device__os_version',
          'event_utc_date_id__date',
          'event_utc_date_id__day',
          'event_utc_date_id__month',
          'event_utc_date_id__year',
          'event_utc_date_id__day_of_week',
          'event_utc_date_id__day_name',
          'event_utc_date_id__week_of_year',
          'event_utc_date_id__quarter',
          'user_id__territory_id__code']
    )

    b.set_map(
        **{
            'user_id__territory_id__code':          'territory_code',
            'client_id__client_id':                 'client_id',
            'event_utc_date_id__date':              'date',
            'event_utc_date_id__year':              'year',
            'event_utc_date_id__month':             'month',
            'event_utc_date_id__day':               'day',
            'event_utc_date_id__day_of_week':       'day_of_week',
            'event_utc_date_id__day_name':          'day_name',
            'event_utc_date_id__week_of_year':      'week_of_year',
            'event_utc_date_id__quarter':           'quarter',
            'platform_id__os':                      'platform_os',
            'platform_id__name':                    'platform_name',
            'platform_id__version':                 'platform_version',
            'device__os':                           'device_os',
            'device__model':                        'device_model',
            'device__make':                         'device_make',
            'device__os_version':                   'device_os_version',
        }
    )

    b.set_unique_values(
        *['client_id__client_id',
          'platform_id__os',
          'platform_id__name',
          'platform_id__version',
          'device__os',
          'device__model',
          'device__make',
          'device__os_version',
          'user_id__territory_id__code',
          'event_utc_date_id__date']
    )

    res, msg = b.build()

    log.info(' COLLECTING FOR : {} ON {}'.format(b._fact, date))
    del b
    gc.collect()

    print msg
