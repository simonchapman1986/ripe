import time
import hashlib
import datetime
from collections import defaultdict

from django.db import models
from django.conf import settings
from django.db import IntegrityError
from django.core.exceptions import FieldError

from apps.base.models.dimensions.dimension_client import DimensionClient
from apps.base.models.dimensions.dimension_platform import DimensionPlatform

from apps.cubes.models import Log

import logging

log = logging.getLogger('trace')

import gc


class MyAgg(object):
    def __init__(self):
        self.total_new = 0


class AggregatorFactory(object):

    def __init__(self, fact=None, agg_fact=None, date=None, ignore_platform=False):
        """
        This is the OLAP builder factory

        The OLAP Builder Factory is to be used to aggregate our FACTS as an inherited class

        simple example to use:

        class ModelClassCube(BuilderFactory):
            # if we wish to override any of the functionality, we can
            # examples of methods of override:
            #    _get_fact() <-- if the fact filter is different than expected - we can alter it here
            #    _builder() <-- only to be done in extreme circumstance / do we really need to override?
            #
            # always check method first before overriding to be clear on your alterations.
            pass


        # first lets instantiate our cube
        cube = FactSubscribedUsersCube(fact=FactModel, agg_fact=AggregatedFactModel, date=None) # None if auto detect

        # now lets set the values/fields we want to return from our fact/dim tables
        # parse args of list
        cube.set_values(*['client_id', 'platform_id'])

        # next we need to build a map, this is to X over our fact/dim field names, to our new cube table names
        # parse kwargs of dict
        cube.set_map(**{'client_id': 'client', 'platform_id': 'platform'})

        # finally we need to set our unique field references.
        # this is to uniquely identify each aggregate row we build
        # for example. Only on client, or client and platform
        # ensure the field references are with the fields, NOT the map
        # parse args of list
        cube.set_unique_values(*['client_id', 'platform_id'])

        # then all we need to do is build
        result = cube.build()

        # True, if successful, False if a failure - exceptions exist
        """
        self._agg = defaultdict(MyAgg)
        self._ignore_platform = ignore_platform
        
        if fact:
            self._fact = fact
        else:
            raise Exception("Missing FACT")

        if agg_fact:
            self._agg_fact = agg_fact
        else:
            raise Exception("No Storage AGG FACT")
        
        if date:
            self._date = date
        else:
            self._date = datetime.datetime.today().strftime("%Y-%m-%d")

        self._date_obj = datetime.datetime.strptime(self._date, '%Y-%m-%d')

        self._values = None
        self._map = None
        self._unique_values = None
        self._filter_fact = None

    def set_values(self, *args):
        """
        this is for telling our model what values/fields we want returned
        fields = ['client_id', 'client_id__name']
        instance.set_values(*fields)
        """
        self._values = args

    def set_unique_values(self, *args):
        """
        to set our unique fields - this is to identify our aggregates
        so if we wanted our aggregates of only a client, or of a client and platform
        li = ['client_id', 'platform_id']
        instance.set_unique_values(*li)
        """
        self._unique_values = args

    def set_map(self, **kwargs):
        """
        to set our map for our method
        dict = {'a_field_name': 'a_field'}
        instance.set_map(**dict)
        """
        self._map = kwargs

    def build(self):
        """
        our callable function

        this will trigger the build
        instance.build()
        """
        if self._values and self._unique_values and self._map:
            if self._builder:
                return True, '{} has been built for date {}'.format(self.__class__, self._date)
            return False, '{} has failed for date {}'.format(self.__class__, self._date)
        return False, '{} has been unable to start build for date {}'.format(self.__class__, self._date)

    def _get_fact(self, dim_client, dim_platform):
        """
        if we need to alter the filter for out builder
        we can override this method if we inherit
        sensibly abstracted
        """
        fact = self._fact.objects.filter(
            user_id__client_id=dim_client,
            platform_id=dim_platform
        )

        # our basic filter for each aggregate
        self._filter_fact = fact

        # the absolute filter we want internally for computation
        fact.filter(event_utc_date_id__date=self._date).values(*('id',))
        re = []
        for value in self._values:
            try:
                re += fact.values(*[value])
            except FieldError:
                pass
        return re

    @property
    def _builder(self):
        """
        if we need to store our aggregate differently
        we can override this method if we inherit
        sensibly abstracted - however this shouldnt be needed
        and should be done with caution
        not properties that exist
        """
        dim_clients = self._get_clients

        if not self._ignore_platform:
            dim_platforms = [a.id for a in DimensionPlatform.objects.all()]
        else:
            dim_platforms = [0]

        for dim_client in dim_clients:
            for dim_platform in dim_platforms:
                fact = self._get_fact(dim_client, dim_platform)

                for row in fact:
                    row, valid = self._preconditions(row)
                    if valid:
                        uuid = ''
                        for arg in self._unique_values:
                            uuid += str(row[arg])

                        m = hashlib.md5()
                        m.update(uuid)
                        uuid = m.hexdigest()
                        # new sums
                        self._sums(uuid, row)

                        for value in self._values:
                            if value in self._map:
                                var = self._agg_fact._meta.get_field_by_name(self._map[value])[0]
                                if isinstance(var, models.CharField):
                                    default = ''
                                elif isinstance(var, models.IntegerField):
                                    default = 0
                                else:
                                    default = ''
                                setattr(self._agg[uuid], self._map[value], default if not row[value] else row[value])
                    del row['id']

        return self._store()

    def _preconditions(self, row):
        """
        if some pre-conditions are required to check against a row of data - or even changes
        then this is the location to override and bring in this logic.

        by default we simply return True as no default preconditions are required.
        """
        return row, True

    @property
    def _get_clients(self):
        return [a.id for a in DimensionClient.objects.all()]

    def _sums(self, uuid, row):
        """
        in the event of additional sums we can override this method
        we pass the row as this may well be needed - by default we count
        """
        self._agg[uuid].total_new += 1
        self._agg[uuid].average_per_day = 0
        self._agg[uuid].breakdown_pct = 0

    def _postconditions(self, key):
        """
        if some pre-conditions are required to check against a row of data - or even changes
        then this is the location to override and bring in this logic.

        by default we simply return True as no default preconditions are required.
        """
        return self._agg[key].__dict__

    def _store(self):
        """
        we store our concluded results here
        """
        for key in self._agg.keys():
            try:
                agg = self._postconditions(key=key)
                assert isinstance(agg, dict)
                data, res = self._agg_fact.objects.get_or_create(**agg)
            except IntegrityError as e:
                raise IntegrityError('for key {}: ({})'.format(key, e.args))
            except FieldError as e:
                raise FieldError('Dict parsed invalid ({})'.format(e.message))
            except Exception as e:
                log.exception('')
                raise e
        return True



class AssertCubeBuild(object):

    def __init__(self, name=None, fact=None, builder=None, async=True):
        if not name:
            raise AttributeError("Missing Build Name")

        if not fact:
            raise AttributeError("Missing Fact for build")

        if not builder:
            raise AttributeError("Missing Builder")

        self.async = async
        self.name = name
        self.fact = fact
        self.builder = builder

    def build(self):

        fact = self.fact.objects.exclude(
            event_utc_date_id__date__in=Log.objects.filter(cube=self.name).values_list('date', flat=True)
        ).exclude(event_utc_date_id__date=datetime.date.today()).values('event_utc_date_id__date').distinct()

        if fact:
            # for each date - run aggregation
            for date in [date['event_utc_date_id__date'].strftime(settings.DATE_FORMAT_YMD) for date in fact]:
                s_date = time.time()
                if not self.async:
                    self.builder(
                        date=date
                    )

                else:
                    self.builder.delay(
                        date=date
                    )
                # log cube
                e_date = time.time()
                try:
                    Log.objects.create(
                        cube=self.name,
                        date=date,
                        time_taken='{:.7f}'.format(e_date-s_date)
                    )
                except Exception as e:
                    log.exception('--Following Exception while logging cube build process during OLAP')
                    raise e
            del self.builder
            gc.collect()

