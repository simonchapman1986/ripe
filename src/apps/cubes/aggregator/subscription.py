from celery.task import task

from apps.base.models import FactServicesStorefrontSubscription
from apps.base.models.dimensions.dimension_subscription_state import DimensionSubscriptionState

from apps.cubes.models import CubeSubscriptionsDaily

from apps.cubes import aggregator as aggregator

from apps.br.subscription import get_rule, RNS

from apps.br.subscription import ignore_event

import datetime

import time

import gc
import logging
log = logging.getLogger('reporting')



class SubscribedUsersCube(aggregator.AggregatorFactory):
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

    def _preconditions(self, row=dict):

        try:
            _row = FactServicesStorefrontSubscription.objects.get(id=row['id'])
        except FactServicesStorefrontSubscription.DoesNotExist:
            # this is fine, as there is no previous row, so we dont need to assert anything
            _row = None

        if _row:

            current_state = FactServicesStorefrontSubscription.get_last_event(
                subscription_id=_row.subscription_id,
                date=_row.event_utc_datetime
            )

            state, err = get_rule(
                status=_row.subscription_status.id,
                current_state=current_state,
                window_ongoing=_row.window.on_going
            )

            _state_obj, _ = DimensionSubscriptionState.objects.get_or_create(state=state)

            _row.subscription_state = _state_obj
            _row.subscription_state_error = err
            _row.save()

            row['subscription_state_id__state'] = state
            row['subscription_state_error'] = err

        del row['subscription_id']

        return row, True

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

        # now lets give this back
        return self._agg[key].__dict__


@task()
def build_aggregate(date=None):
    b = SubscribedUsersCube(
        fact=FactServicesStorefrontSubscription,
        agg_fact=CubeSubscriptionsDaily,
        date=date
    )

    b.set_values(
        *[
          'subscription_id',
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
          'subscription_state_id__state',
          'subscription_state_error',
          'window_id',
          'window_id__item_id',
          'window_id__product_id',
          'window_id__pricing_id',
          'window_id__usage_right_id',
          'window_id__tier',
          'window_id__window_type',
          'window_id__on_going',
          'window_id__repeat_count',
          'window_id__auto_upgrade',
          'window_id__allow_repurchase',
        ]
    )

    b.set_map(
        **{
            'user_id__territory_id__code':          'territory_code',
            'user_id__client_id__client_id':        'client_id',
            'subscription_status_id__description':  'subscription_status',
            'subscription_state_id__state':         'subscription_state',
            'subscription_state_error':             'subscription_state_error',
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
            'window_id__item_id':                   'window_item_id',
            'window_id__product_id':                'window_product_id',
            'window_id__pricing_id':                'window_pricing_id',
            'window_id__usage_right_id':            'window_usage_right_id',
            'window_id__tier':                      'window_tier',
            'window_id__window_type':               'window_type',
            'window_id__on_going':                  'window_on_going',
            'window_id__repeat_count':              'window_repeat_count',
            'window_id__auto_upgrade':              'window_auto_upgrade',
            'window_id__allow_repurchase':          'window_allow_repurchase',
        }
    )

    b.set_unique_values(
        *['user_id__client_id__client_id',
          'platform_id__name',
          'user_id__territory_id__code',
          'window_id',
          'subscription_status_id__description',
          'subscription_state_id__state',
          'subscription_state_error',
          'event_utc_date_id__date']
    )

    res, msg = b.build()
    del b
    gc.collect()
    print msg
