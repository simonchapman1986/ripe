from django.db import models
from django_extensions.db.fields import UUIDField
from apps.api.exception import RipeApiException
from django.db.models import Sum
from django.db.models import Min
from django.db.models import Max
from django.db.models import Count


import logging
import datetime


log = logging.getLogger('trace')
db = logging.getLogger('db')


DT_FORMAT = "%Y-%m-%d"


class CubeRegistrationsDaily(models.Model):
    """
    indexes sit on the values we will be filtering on
    these indexes are relational to the dim tables from
    which the aggregated data derives

    DO NOT add indexes to any of these rows using the conventional django method.
    They have been specifically added via South to enable the choice of INDEX type
    In this case the majority of the required indexes are HASH due to only matching exact.
    The cases where equality is required, have BTREE indexes applied (mainly date related).

    Please see the initial cube migration for further reference on the indexing of
    this table, and how to follow suit to add/delete/alter if and when required for
    future migrations.
    """

    # objects = models.Manager()


    # index
    id = UUIDField(version=4, primary_key=True)

    # dim_territory
    territory_code = models.CharField(max_length=10)

    # dim_client
    client_id = models.CharField(max_length=36)

    client_name = models.CharField(max_length=36)

    # dim_utc_date
    date = models.DateField()
    year = models.SmallIntegerField()
    month = models.SmallIntegerField()
    day = models.SmallIntegerField()
    day_of_week = models.IntegerField()
    day_name = models.CharField(max_length=9)
    week_of_year = models.SmallIntegerField()
    quarter = models.SmallIntegerField()

    # dim_platform
    platform_os = models.CharField(max_length=255)
    platform_name = models.CharField(max_length=255)
    platform_version = models.CharField(max_length=255)

    # dim_device
    device_os = models.CharField(max_length=255)
    device_model = models.CharField(max_length=255)
    device_make = models.CharField(max_length=255)
    device_os_version = models.CharField(max_length=255)

    # agg data - not indexes - these are what we are after from the query
    total = models.IntegerField(default=0)
    total_new = models.IntegerField(default=0)
    average_per_day = models.IntegerField(default=0)
    change = models.IntegerField(default=0)
    breakdown_pct = models.IntegerField(default=0)

    created = models.DateTimeField(auto_created=True, auto_now=True, default=datetime.datetime.now())

    class Meta:
        app_label = 'cubes'
        db_table = 'summary_registrations_daily'



    @classmethod
    def get_total(cls, start, end, filters=None, group=None):

        log.info('----IN CUBE: --------{}  {}  {}  {}'.format(filters, start, end, group))

        cls.cubes = cls.filter_registrations(filters=filters, start=start, end=end)
        if group == 'all':
            return CubeRegistrationsDaily.total_summary(cls.cubes, start, end)
        else:
            log.info('--getting registration data grouped by {}---'.format(group))
            return CubeRegistrationsDaily.get_grouped_total_summary(
                filters,
                start,
                end,
                group
            )

    @classmethod
    def total_summary(cls, cube_qs, start, end):
        """
        >>> CubeRegistrationsDaily().get_cubes()
        {'new': 11, 'average': 0.0}
        >>> CubeRegistrationsDaily().get_cubes(territory='GB')
        {'new': 9, 'average': 0.0}
        >>> CubeRegistrationsDaily().get_cubes(client='26c71f59-3069-4e45-bc22-f98b58e8170d')
        {'new': 5, 'average': 0.0}
        >>> CubeRegistrationsDaily().get_cubes(territory='GB', client='26c71f59-3069-4e45-bc22-f98b58e8170d')
        {'new': 3, 'average': 0.0}
        >>> CubeRegistrationsDaily().get_cubes(start_date='2013-11-27')
        {'new': 11, 'average': 0.0}
        >>> CubeRegistrationsDaily().get_cubes(end_date='2013-11-27')
        {'new': 11, 'average': 0.0}
        >>> CubeRegistrationsDaily().get_cubes(start_date='2013-11-27', end_date='2013-11-27')
        {'new': 11, 'average': 0.0}
        >>> CubeRegistrationsDaily().get_cubes(start_date='2099-12-31')
        {'new': None, 'average': None}
        """

        if start == end:
            res = cube_qs \
                .aggregate(
                    new=models.Sum('total_new'),
                    average=models.Avg('average_per_day'),
                    total=Sum('total')
                )
        else:
            res = cube_qs \
                .aggregate(
                    new=models.Sum('total_new'),
                    average=models.Avg('average_per_day'),
                )

            last_day_total = cube_qs.filter(
                date=end
            ).aggregate(
                total=Sum('total')
            )['total']
            res['total'] = last_day_total

            summary = list()
            summary.append(res)
        return summary

    @classmethod
    def filter_registrations(cls, filters, start='all', end='all'):

        try:
            cls.cubes = CubeRegistrationsDaily.objects.all()
            cls.cubes = cls.cubes.filter(date__gte=start).filter(date__lte=end)
        except Exception:
            log.exception('\n\n')

        try:
            if isinstance(filters, dict):
                try:
                    if len(cls.cubes) and len(filters):
                        keys = filters.keys()
                        if 'territory' in keys:
                            cls.cubes = cls.cubes.filter(territory_code=filters['territory'])
                        if 'client_id' in keys:
                            cls.cubes = cls.cubes.filter(client_id=filters['client_id'])
                        if 'platform' in keys:
                            cls.cubes = cls.cubes.filter(platform_name=filters['platform'])
                    else:
                        log.info('--no cube after filters')
                except Exception:
                    log.exception('\n---\n')
            else:
                #todo return exception
                log.info('filters not a dict')
        except Exception:
            log.exception('EXCEPTION OCCURRED')
        return cls.cubes

    @classmethod
    def get_group_name(cls, group):
        allgroups = {'platform': 'platform_name',
                     'client': 'client_id',
                     'territory': 'territory_code',
                     'device': 'device_make',
                     }
        group_name = allgroups.get(group, 'None')
        if not group_name:
            log.info('GROUP NOT FOUND IN DB FOR {}'.format(group))
        return group_name



    @classmethod
    def get_groups(cls, group):
        group_name = cls.get_group_name(group)

        try:
            groups = cls.objects.values(group_name).annotate(new=Count('total_new'))
            log.info('=======GQS: =========  {}'.format(groups))
            return groups, group_name
        except Exception:
            log.exception('\n\n')
        return groups, group_name

    @classmethod
    def get_grouped_total_summary(cls, filters, s, e, group_param):

        all_groups, group_name = cls.get_groups(group_param)

        log.info(' GROUP: {} :: {}'.format(group_param, group_name))
        log.info('-----{}'.format(len(cls.cubes)))

        db.info('------------------\nFILTERS: {} \ns: {} e: {}\n all-groups: {} \ngroup {} -- group_name: {}'.format(
            filters, s, e, all_groups, group_param, group_name)
        )


        try:
            # cls.cubes = cls.filter_registrations(filters=filters, start=s, end=e)

            #trace
            db.info('----FILTERED CUBE-----')
            # for c in cls.cubes:
            #     db.info('dt: {} p:{} t: {} n: {} a: {} territory: {} device_make: {}'.format(
            #         c.date,
            #         c.platform_name,
            #         c.total,
            #         c.total_new,
            #         c.average_per_day,
            #         c.territory_code,
            #         c.device_make))
            #trace

            filtered_groups = cls.filter_all_groups(filters, all_groups, group_param, group_name)
        except Exception:
            db.exception('\n-----\n')

        try:
            data = dict()
            group_summary = dict()
            for group_data in filtered_groups:
                # db.info('-----------GROUP-NAME: {}: GROUP-DATA: {}\n'.format(group_name, group_data))
                res = {}
                tot = 0
                if group_name in group_data:
                    if group_name == 'platform_name':
                        try:

                            # trace.info('\n\n===============GROUP NAME: {}\n\n'.format(group_data[group_name]))
                            # trace.info('>>>>>>>>>>>>>>>>>> LEN: c: {}'.format(len(cls.cubes)))

                            # for c in cls.cubes:
                            #     trace.info('pn: {} tot: {} tn: {}'.format(c.platform_name, c.total, c.total_new))


                            x = cls.cubes.filter(platform_name=group_data[group_name])

                            # trace.info('>>>>>>>AFTER FILTER>>>>>>>>>>> LEN: C: {}'.format(len(x)))

                            # for c in cls.cubes:
                            #     trace.info('pn: {} tot: {} tn: {}'.format(c.platform_name, c.total, c.total_new))
                            #
                            # for c in x:
                            #     trace.info('xxxxxxxx    pn: {} tot: {} tn: {}'.format(c.platform_name, c.total, c.total_new))

                            res = cls.total_summary(x, s, e)
                            tot = res['total']

                            # trace.info('===========RES====================: {} TOT: {}\n'.format(
                            #     res, tot)
                            # )
                        except Exception:
                            db.exception('---filtering by {} --- '.format(group_data[group_name]))
                            #TODO
                    elif group_name == 'territory_code':
                        try:
                            # tot = cls.cubes.filter(territory_code=group_data[group_name]).latest('date').total
                            # res = cls.cubes.filter(territory_code=group_data[group_name]).aggregate(
                            #     new=Sum('total_new'),
                            #     average=models.Avg('average_per_day')
                            # )

                            # - temp. behaviour confirmation required here.
                            x = cls.cubes.filter(territory_code=group_data[group_name])
                            res = cls.total_summary(x, s, e)
                            tot = res['total']



                        except Exception:
                            db.exception('---filtering by {} --- '.format(group_data[group_name]))
                    elif group_name == 'device_make':

                        try:
                            # tot = cls.cubes.filter(device_make=group_data[group_name]).latest('date').total
                            # res = cls.cubes.filter(device_make=group_data[group_name]).aggregate(
                            #     new=Sum('total_new'),
                            #     average=models.Avg('average_per_day')
                            # )
                            x = cls.cubes.filter(device_make=group_data[group_name])
                            res = cls.total_summary(x, s, e)
                            tot = res['total']

                        except Exception:
                            db.info('\n{}\n'.format())
                            db.exception('---filtering by {} --- '.format(group_data[group_name]))

                    res['total'] = int(tot)
                    db.info('----------------DATA for group {}:{} =  {}'.format(group_name, group_data[group_name], res))
                    group_summary.update({str(group_data[group_name]): res})
            data.update(group_summary)
            db.info('---------GROUP RES: {}'.format(data))
            return data
        except Exception:
            db.exception('\n')


    @classmethod
    def filter_all_groups(cls, filters, all_groups, group_by, group_name):
        # group_name = cls.get_group_name(group_by)
        # all_groups = dict()
        # all_groups.update(groups)

        group_list = list()
        for g in all_groups:
            group_list.append(g)
        # db.info('----GROUP LIST----------{}'.format(group_list))
        try:
            # db.info(' -----------ALL GROUPS-------------: {}'.format(all_groups))
            if group_by in filters:
                #filtered-group --- group=filter
                for g in group_list:
                    if g[group_name] != filters[group_by]:
                        del group_list[group_list.index(g)]
                        # db.info('++++{}'.format(type(all_groups)))
            else:
                # filtered-group, filter != group
                for g in group_list:
                    if group_by == 'device':
                        filtered_cube_group_val = cls.cubes.filter(device_make=g['device_make'])
                    elif group_by == 'territory':
                        filtered_cube_group_val = cls.cubes.filter(territory_code=g['territory_code'])
                    elif group_by == 'platform':
                        filtered_cube_group_val = cls.cubes.filter(platform_name=g['platform_name'])

                    if not len(filtered_cube_group_val):
                        del group_list[group_list.index(g)]


            db.info(' ALL GROUPS AFTER FILTER: {}'.format(group_list))
        except Exception:
            db.exception('\n')
        return group_list

    @classmethod
    def test(cls):
        return 'just a test'
