from celery.task import task

from apps.base.models import FactServicesStorefrontTransaction

from apps.cubes.models import CubeStoreTransaction

from apps.cubes import aggregator as aggregator

from decimal import Decimal

from apps.base.models import Clients


import logging
log = logging.getLogger('reporting')


class StoreTransactionCube(aggregator.AggregatorFactory):
    """
    if we wish to override any of the functionality, we can
    examples of methods of override:
        _get_fact() <-- if the fact filter is different than expected - we can alter it here
        _builder() <-- only to be done in extreme circumstance / do we really need to override?

    always check method first before overriding to be clear on your alterations.
    """

    def _get_fact(self, dim_client, dim_platform):

        fact = self._fact.objects.filter(
            user_id__client_id=dim_client
        )

        # our basic filter for each aggregate
        self._filter_fact = fact

        # the absolute filter we want internally for computation
        return fact.filter(event_utc_date_id__date=self._date).values(*self._values+('id',))

    def _sums(self, uuid, row):
        """
        in the event of additional sums we can override this method
        we pass the row as this may well be needed - by default we count
        """
        self._agg[uuid].total_new += 1
        self._agg[uuid].average_per_day = 0
        self._agg[uuid].breakdown_pct = 0
        # self._agg[uuid].change = 0  # this field does not exist in the related cube.
        self._agg[uuid].total = 0
        self._agg[uuid].total_price = 0
        # self._agg[uuid].total_price_day += row['price']  # attribute cannot be used and created at the same time.
        #TODO set attribute if it does not exist. update it if exists.
        self._agg[uuid].total_price_day = row['price']

    def _postconditions(self, key):
        # shallow copy dict (however this copies the iterator - beware)
        dic = self._agg[key].__dict__
        # # remove date attributes as we dont want to filter this... + a couple others
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
        #     'change',
            'total',
            'total_price',
            'total_price_day',
        ]

        # we are going to store these values for a short period
        temp_store = {}

        # if we have no average, our average will equal that of the total new
        p_avg = dic['total_new']

        tp_avg = dic['total_price_day']

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
        tp = Decimal(0.00)
        for r in res:
            t+=r.total_new
            last = r.total
            tp+=r.total_price_day

        total = t+p_avg
        total_price = tp+tp_avg

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
        self._agg[key].total_price = total_price

        #TODO - required for transactions?
        # we give a churn here..
        # try:
        #     self._agg[key].change = total - last
        # except:
        #     self._agg[key].change = 0

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
    b = StoreTransactionCube(
        fact=FactServicesStorefrontTransaction,
        agg_fact=CubeStoreTransaction,
        date=date,
        ignore_platform=True)

    b.set_values(
        *[
            'item__item_title',
            'item__item_id',
            'product__product_id',
            'window__window_id',
            'transaction_status__description',
            'right__right_id',
            'price',
            'currency__code',
            'retail_model__model',
            'definition__definition',
            'client__client_id',
            'territory__code',
            'platform__os',
            'platform__name',
            'platform__version',
            'device__device_id',
            # date fields
            'event_utc_date__date',
            'event_utc_date__day',
            'event_utc_date__month',
            'event_utc_date__year',
            'event_utc_date__day_of_week',
            'event_utc_date__day_name',
            'event_utc_date__week_of_year',
            'event_utc_date__quarter',
            'user__external_user_id',
            'user__first_name',
            'user__last_name',
            'last_4_digits',
            'retail_model__model'
        ]
    )

    b.set_map(
        **{
            'item__item_title':                     'item_title',
            'product__product_id':                  'product_id',
            'window__window_id':                    'window_id',
            'transaction_status__description':      'transaction_status',
            'right__right_id':                      'right_id',
            'currency__code':                       'currency_code',
            'retail_model__model':                  'retail_model',
            'definition__definition':               'definition',
            'client__client_id':                    'client_id',
            'territory__code':                      'territory_code',
            'platform__os':                         'platform_os',
            'platform__name':                       'platform_name',
            'platform__version':                    'platform_version',
            'device__device_id':                    'device_id',
            'event_utc_date__date':                 'date',
            'event_utc_date__year':                 'year',
            'event_utc_date__month':                'month',
            'event_utc_date__day':                  'day',
            'event_utc_date__day_of_week':          'day_of_week',
            'event_utc_date__day_name':             'day_name',
            'event_utc_date__week_of_year':         'week_of_year',
            'event_utc_date__quarter':              'quarter',
            'user__external_user_id':               'external_user_id',
            'user__first_name':                     'first_name',
            'user__last_name':                      'last_name',
            'price':                                'total_price_day',
            'item_item_id':                         'item_id',
            'last_4_digits':                        'last_4_digits',
            'content_type':                         'content_type',
            'retail_model__model':                  'retail_model'

        }
    )

    b.set_unique_values(
        *['item__item_id',
          'product__product_id',
          'window__window_id',
          'transaction_status__description',
          'right__right_id',
          'currency__code',
          'retail_model__model',
          'definition__definition',
          'client__client_id',
          'territory__code',
          'platform__os',
          'platform__name',
          'platform__version',
          'device__device_id',
          'event_utc_date__date']
    )

    res, msg = b.build()
    print msg