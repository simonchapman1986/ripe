from apps.api.exception import RipeApiException

from apps.br.subscription import RNS
from apps.br.subscription import SF
from apps.br.subscription import SO
from apps.br.subscription import WSL
from apps.br.subscription import WSC
from apps.br.subscription import WSLI
from apps.br.subscription import WSCI
from apps.br.subscription import WSE

from apps.br.subscription import user_sub_not_ongoing
from apps.br.subscription import user_sub_ongoing

from django.core.exceptions import ObjectDoesNotExist

from django.db import models
from django.db.models import Q
from django.db.models import Sum
from django.db.models import Min
from django.db.models import Max
from django.db.models import Count

from collections import OrderedDict
from apps.api.helpers.dates import month_end

import datetime
import logging
import calendar
import copy




logger = logging.getLogger('reporting')
trace = logging.getLogger('reporting')


class SubscriptionManager(models.Manager):

    DTFORMAT = '%Y-%m-%d'
    DEFAULT_RESPONSE = {
        'new': 0,
        'total': 0,
        'average': 0
    }
    DEFAULT_GROUP_RESPONSE = {
        '': {
                'new': 0,
                'total': 0,
            }
    }



    def __init__(self):
        self.event_states = []
        self.states = [SF, SO, RNS, WSL, WSC, WSCI, WSLI, WSE]
        self.pack = user_sub_ongoing
        super(SubscriptionManager, self).__init__()

    def get_queryset(self):
        return super(SubscriptionManager, self).get_queryset()

    def filter_cube(self, filters):
        sub = self.model.objects.all()

        sub.exclude(subscription_state__in=self.states)
        if isinstance(filters, dict):
            if len(sub) and len(filters):

                print '\n FILTERING START subs len: {}   filters len: {}, filters: {}'.format(len(sub), len(filters), filters)

                keys = filters.keys()
                if 'user_state' in keys:
                    if 'package' in keys:

                        if filters['package'] == 'all':
                            package = [1, 0]
                        elif filters['package'] == 'ongoing':
                            package = [1]
                        elif filters['package'] == 'fixed':
                            package = [0]
                        else:
                            raise RipeApiException(
                                *RipeApiException.MODEL_BAD_SUBSCRIPTION_PACKAGE,
                                debug_message=u'Invalid Package Filter for subscriptions ({})'.format(
                                    filters['package'])
                            )

                        sub = sub.filter(window_on_going__in=package)

                        if package[0] == 1:
                            self.pack = user_sub_ongoing

                        if package[0] == 0:
                            self.pack = user_sub_not_ongoing

                        if len(package) == 2:
                            self.pack = user_sub_not_ongoing+user_sub_ongoing

                        state = False
                        self.event_states = []
                        for _, n, event in self.pack:
                            if event == filters['user_state']:
                                state = True
                                self.event_states.append(n)

                        sub = sub.filter(
                            reduce(lambda q, f: q | Q(subscription_state=f), self.event_states, Q())
                        )

                        if not state:
                            raise RipeApiException(
                                *RipeApiException.MODEL_BAD_SUBSCRIPTION_STATE,
                                debug_message=u'Invalid State Filter for subscriptions ({})'.format(
                                    filters['user_state'])
                            )

                    if 'territory' in keys:
                        sub = sub.filter(territory_code=filters['territory'])
                    if 'client' in keys:
                        sub = sub.filter(client_id=filters['client'])
                    if 'platform' in keys:
                        sub = sub.filter(platform_name=filters['platform'])
        return sub

    def total(self, filters, group, start_date='all', end_date=None):


        subscriptions = self.filter_cube(filters)
        subscriptions = self.filter_by_dates(start_date, end_date, subscriptions)

        if not len(subscriptions):
            default = self.DEFAULT_RESPONSE if group == 'all' else self.DEFAULT_GROUP_RESPONSE
            return default

        res = self.DEFAULT_RESPONSE

        # period based total filter
        subs = subscriptions.filter(subscription_status=filters['user_state'])

        if end_date == 'all':
            end_date = subs.aggregate(Max('date'))['date__max']


        try:
            active = subs.exclude(date__gt=end_date).aggregate(new=Sum('total_new'))['new']
        except ObjectDoesNotExist:
            active = 0
        except IndexError:
            active = 0

        res['new'] = active

        # total since beginning of time calculated by filter, and not other states
        try:
            states = list(OrderedDict.fromkeys(self.event_states))
            total_is = 0
            for state in states:
                total_is += subscriptions.filter(
                    subscription_status=filters['user_state']
                ).filter(
                    subscription_state=state
                ).exclude(
                        date__gt=end_date
                ).latest('date').total
        except ObjectDoesNotExist:
            total_is = 0

        # GROUPS. churn not taken
        if group:
            if group != 'all':
                return self.get_groups(filters, group, subscriptions.filter(
                    subscription_status=filters['user_state']).exclude(date__gt=end_date))

        current_filter_state = filters['user_state']
        lapcan = 0

        try:
            trace.info('<<<<<<<<<<  LOST SUBS  <<<<<<<<<<<<<')
            total_not = 0
            _filters = ['expired', 'cancelled', 'lapsed', 'active']
            for k, v in enumerate(_filters):
                if v == current_filter_state:
                    _filters.pop(k)
                if current_filter_state == 'active' and v == 'inactive':
                    _filters.pop(k)
            for fil in _filters:
                filters['user_state'] = fil
                tot_not_act = self.filter_cube(filters)
                tot_not_act = self.filter_by_dates(start_date, end_date, tot_not_act)
                try:
                    exclude_total = tot_not_act.exclude(date__gt=end_date).latest('date').total
                    # total_not += tot_not_act.exclude(
                    #     date__gt=end_date).latest('date').total
                    trace.info('exclude total for FILTER: {}: {}'.format(fil, exclude_total ))
                    total_not += exclude_total
                except:
                    pass
                if fil == 'lapsed' or fil == 'cancelled':
                    lapcan += total_not
                    trace.info('LAPCAN/CHURN: {}'.format(lapcan))
            trace.info('>>>>>>>>>>>>>>>>>LOST SUBS>>>>>>>>>>>>>>>>>>>>>>>>')
        except ObjectDoesNotExist:
            trace.exception('\n******WHILE CAL TOTAL TO EXCLUDE********\n')
            total_not = 0

        tots = total_is-total_not
        trace.info('TOTAL: {}, EX-TOTAL: {}, FINAL TOTAL: {}'.format(total_is, total_not, tots))

        filters['user_state'] = current_filter_state
        res['total'] = tots
        res['churn'] = lapcan

        if lapcan:
            percent = (lapcan / float(total_is))
            percent = percent * 100
            res['churn_pct'] = float("{0:.2f}".format(percent))
        else:
            res['churn_pct'] = 0

        try:
            res['average'] = res['new'] / len(subs)
        except TypeError:
            res['new'] = 0
            res['average'] = 0

        return res

    @staticmethod
    def filter_by_dates(start, end, obj):
        try:
            if start != 'all':
                start = datetime.datetime.strptime(start, '%Y-%m-%d').date()
                if end is None or end == 'all':
                    end = obj.aggregate(Max('date'))['date__max']
                else:
                    end = datetime.datetime.strptime(end, '%Y-%m-%d').date()
                obj = obj.filter(date__gte=start).filter(date__lte=end)

        except ValueError:
            raise RipeApiException(
                *RipeApiException.MODEL_BAD_DATE_FORMAT,
                debug_message=u'Invalid date format'
            )
        return obj

    @staticmethod
    def get_groups(filters, group, obj):

        result = {}

        try:
            # group_name = group
            print 'GROUP : {}' .format(group)
            if group != 'all':
                allgroups = {'platform': 'platform_name',
                             'client': 'client_id',
                             'territory': 'territory_code',
                             'package': 'window_on_going',
                             'user_state': 'subscription_state'}
                group_name = allgroups.get(group)

            trace.info('\n group: {} group_name: {}'.format(group, group_name))

            maps = {'platform': 'platform_name',
                    'client': 'client_id',
                    'territory': 'territory_code',
                    'package': 'subscription_state',
                    'user_state': 'subscription_state'}
            # trace.info('\n FILTERS: {}\n'.format(filters))

            #convert filters to model based names

            maped_filters = {}
            maped_filters.update(filters)

            for f in filters:
                # trace.info('mapping filter: {} {}'.format(f, filters[f]))
                if f in maps:
                    if f != 'user_state':
                        maped_filters[maps[f]] = filters[f]
                        del maped_filters[f]
            # trace.info('\n FILTERS MAPPED TO MODEL: {}\n'.format(maped_filters))

            # if 'package' in filters:
            #     filters['subscription_state'] = filters['package']
            #     del filters['package']
        except Exception:
            trace.exception('\n>>>>>\n')

        res = ''
        try:
            res = obj.values(group_name).annotate(total=Sum('total_new'), new=Sum('total_new'))
            # res = obj.values(group_name).annotate(total=Sum('total_new'), new=Sum('total_new')).values('total', 'new')
            # res = obj.values(group_name).annotate().values('total', 'new')
        except Exception:
            trace.exception('\n\n')

        trace.info('>>>>>>>>>>>>>>>>>')
        trace.info(' GROUPED BY : {}\n {} AGG RESULT: {}'.format(group_name, type(res), res))
        trace.info('>>>>>>>>>>>>>>>>>')


        i = 0
        for d in res:
            trace.info('>>>>>>>>> {}'.format(d))
            id = i
            #if 'subscription_status' not in d.keys():
            #    d['new'] = d['total']
            if 'territory_code' in d.keys() and 'territory_code' == group_name:
                id = d.pop('territory_code', None)
            elif 'window_on_going' in d.keys() and 'window_on_going' == group_name:
                id = 'ongoing' if d.pop('window_on_going', False) else 'fixed'
            elif 'date' in d.keys() and 'date' == group_name:
                d['date'] = datetime.datetime.strftime(d['date'], '%Y-%m-%d')
            elif 'platform_name' in d.keys() and 'platform_name' == group_name:
                id = d.pop('platform_name', -1)
            # if id in result.keys():
            #     result[id]['new'] += d['new']
            # else:
            result[id] = d
            i += 1

        # trace.info('FINAL RESULT AFTER GROUPS: \n {}\n {}\n'.format(type(result), result))


        return result

    #MONTHLY
    def monthly(self, filters=None, group=None, start_date='all', end_date=None):
        dt_filtered_cube = self.filter_cube(filters)
        dt_filtered_cube = self.filter_by_dates(start_date, end_date, dt_filtered_cube)
        res = OrderedDict()
        i = 0
        start_dt = dt_filtered_cube.aggregate(Min('date'))['date__min']
        end_dt = dt_filtered_cube.exclude(date__gt=end_date).aggregate(Max('date'))['date__max']

        end_increment = month_end(start_dt)
        while end_increment <= end_dt:
            resd = dict()
            structure = self.total(
                filters, group, start_dt.strftime(self.DTFORMAT), end_increment.strftime(self.DTFORMAT))

            # trace.info('---MONTHLY TOTAL: {}\n\n'.format(structure))
            if structure:
                if 'churn' in structure:
                    resd['churn'] = structure['churn']
                if 'churn_pct' in structure:
                    resd['churn_pct'] = structure['churn_pct']
                if 'average' in structure:
                    resd['average'] = structure['average']
                if 'new' in structure:
                    resd['new'] = structure['new']
                if 'total' in structure:
                    resd['total'] = structure['total']
                if len(resd) == 0:
                    resd = structure
                resd['name'] = start_dt.strftime("%b")
                resd['start'] = str(start_dt)
                resd['end'] = str(end_increment)
                res[i] = resd
                i += 1
            start_dt = end_increment+datetime.timedelta(days=1)
            end_increment = month_end(start_dt)
        trace.info('\n----MONTHLY SUMMARY: \n{}\n'.format(res))
        return res

    #weekly
    def weekly(self, filters=None, group=None, start_date='all', end_date=None):
        res = OrderedDict()
        i = 0
        if start_date != 'all':
            start_dt = datetime.datetime.strptime(start_date, self.DTFORMAT).date()
            if end_date:
                end_dt = datetime.datetime.strptime(end_date, self.DTFORMAT).date()
            else:
                end_dt = self.cube.aggregate(Max('date'))['date__max']
        else:
            start_dt = self.cube.aggregate(Min('date'))['date__min']
            end_dt = self.cube.aggregate(Max('date'))['date__max']

        seven = datetime.timedelta(days=7)
        end_increment = start_dt + +datetime.timedelta(days=6)
        while end_increment <= end_dt:
            resd = dict()
            structure = self.total(filters,
                                   group=group,
                                   start_date=start_dt.strftime(self.DTFORMAT),
                                   end_date=end_increment.strftime(self.DTFORMAT))

            # trace.info('---WEEKLY TOTAL: {}\n\n'.format(structure))
            if structure:
                if 'churn' in structure:
                    resd['churn'] = structure['churn']
                if 'churn_pct' in structure:
                    resd['churn_pct'] = structure['churn_pct']
                if 'average' in structure:
                    resd['average'] = structure['average']
                if 'new' in structure:
                    resd['new'] = structure['new']
                if 'total' in structure:
                    resd['total'] = structure['total']
                if len(resd) == 0:
                    resd = structure
                resd['name'] = start_dt.strftime("%W")
                resd['start'] = str(start_dt)
                resd['end'] = str(end_increment)
                res[i] = resd
                i += 1
            start_dt = start_dt + seven
            end_increment = end_increment + seven
            #last week might be shorter than the end_date
            if start_dt <= end_dt < end_increment:
                end_increment = end_dt

        trace.info('\n----WEEKLY SUMMARY: \n{}\n'.format(res))

        return res


    def get_month_interval(self, start, rem):
        """
        >>> get_month_interval(datetime.date(2014, 02, 11), 5)
        (datetime.date(2014, 2, 15), 0, False)
        >>> get_month_interval(datetime.date(2014, 01, 31), 40)
        (datetime.date(2014, 2, 16), 0, True)
        >>> get_month_interval(datetime.date(2014, 03, 01), 11)
        (datetime.date(2014, 2, 16), 0, True)

        """
        end_of_month = datetime.date(start.year, start.month, calendar.monthrange(start.year, start.month)[1])
        end = start
        c = rem
        rem -= 1
        for i in range(1, c):
            end = end+datetime.timedelta(days=1)
            rem -= 1
            if end == end_of_month:
                return end, rem, True
        return end, rem, False

    def get_weekly_date_range(self, start_date, number_of_weeks):
        """
        >>> CubeFactSubscribedUsers.get_weekly_date_range('2014-02-23', 2)
        [['2014-02-23', '2014-03-01'], ['2014-03-02', '2014-03-08']]
        >>> CubeFactSubscribedUsers.get_weekly_date_range('2014-12-31', 1)
        [['2014-12-31', '2015-01-06']]
        """
        if not start_date or not number_of_weeks:
            logger.info('  {}  {}'.format(start_date, number_of_weeks))
            #todo
            raise Exception('no start date or number of weeks')
        if isinstance(start_date, str):
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        if start_date > datetime.date.today():
            #todo
            raise Exception('start date in the future')
        date_range = []
        for w in range(number_of_weeks):
            end_date = start_date+datetime.timedelta(days=6)
            date_range.append([start_date, end_date])
            start_date = end_date+datetime.timedelta(days=1)
        return date_range

    def daily_summary(self, filters=None, group=None, st_date='all', end_date=None):
        # trace.info('-->>>>>>>>>>>>>>>>>>>>>>>>>----------------{}---{}\n'.format(st_date, end_date))
        dt_filtered_cube = self.filter_cube(filters)
        dt_filtered_cube = self.filter_by_dates(st_date, end_date, dt_filtered_cube)

        summary = {}
        if len(dt_filtered_cube):
            start_dt = dt_filtered_cube.aggregate(Min('date'))['date__min']
            end_dt = dt_filtered_cube.exclude(date__gt=end_date).aggregate(Max('date'))['date__max']

            daily_dates = ''
            try:
                daily_dates = [start_dt+datetime.timedelta(days=i) for i in range((end_dt-start_dt).days+1)]
            except Exception:
                trace.exception('\n\n')
        else:
            daily_dates = [datetime.datetime.strptime(st_date, '%Y-%m-%d').date()]

        # trace.info('DAILY DATES: \n{}\n'.format(daily_dates))

        day = 0
        for dt in daily_dates:
            dtstr = dt.strftime(self.DTFORMAT)
            resd = dict()
            res = self.total(
                filters, group, dtstr, dtstr)

            trace.info('--------DAILY----------{}'.format(res))

            if 'new' in res:
                resd['new'] = res['new']
            if 'total' in res.keys():
                resd['total'] = res['total']
            if 'churn' in res:
                resd['churn'] = res['churn']
            if 'churn_pct' in res:
                resd['churn_pct'] = res['churn_pct']
            if 'average' in res:
                resd['average'] = res['average']
            if len(resd) == 0:
                resd = res
            resd['name'] = dt.strftime("%A")
            resd['start'] = dtstr
            resd['end'] = dtstr

            summary[day] = resd
            day += 1


        trace.info('\n----DAILY SUMMARY: \n{}\n'.format(summary))
        return summary

