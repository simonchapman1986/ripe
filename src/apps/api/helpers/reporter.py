import datetime
from apps.cubes.models.daily.subscriptions import CubeSubscriptionsDaily
from apps.cubes.models.daily.registrations import CubeRegistrationsDaily

# from apps.reporting.models import CubeFactRegisteredUsers
from django.db.models import Sum
from django.db.models import Min
from django.db.models import Max
import calendar


import logging
logger = logging.getLogger('reporting')


class Reporter():

    DTFORMAT = '%Y-%m-%d'

    def __init__(self, cls, client_id):
        """
        >>> r = Reporter(CubeSubscriptionsDaily, 'b7ff76fd-e078-483a-8318-040a92df7dc9')
        1
        """
        self.cls = cls
        self.client_id = client_id
        self.cube = self.cls.objects.filter(client_id=self.client_id)

    def get_monthly_total(self, st_date, rem=None):
        """
        # >>> get_monthly_total(datetime.date(2014, 02, 11), 5)
        # 1
        # >>> get_monthly_total(datetime.date(2014, 02, 11), 10)
        # 1
        # >>> get_monthly_total(datetime.date(2014, 02, 11), 35)
        # 1
        # >>> get_monthly_total('2014-11-02', 65, 'b7ff76fd-e078-483a-8318-040a92df7dc9')
        # {0: {'end': '2014-03-11', 'start': '2014-02-11', 'total': 412, 'breakdown_pct': 0}, 1: {'end': '2014-04-12', 'start': '2014-03-12', 'total': None, 'breakdown_pct': None}, 'days': {'end': '2014-04-16', 'start': '2014-04-13', 'total': None, 'breakdown_pct': None}}
        >>> get_monthly_total('all', None)
        1

        """
        res = {}
        i = 0

        if st_date != 'all':
            st_date = datetime.datetime.strptime(st_date, self.DTFORMAT).date()
        else:
            st_date = self.cube.aggregate(Min('date'))['date__min']
            max = self.cube.aggregate(Max('date'))['date__max']
            rem = int((max-st_date).days) + 1    # include the start date.

        while rem:
            end, rem, is_month_end = self.get_month_interval(st_date, rem)
            logger.info('s: {} e:{} rem:{} me: {}'.format(st_date, end, rem, is_month_end))
            self.cube = self.cls.objects.filter(client_id=self.client_id)
            total = self.sum_cube(st_date, end)
            total['start'] = str(st_date)
            total['end'] = str(end)
            if is_month_end:
                res[i] = total
            else:
                res['days'] = total
            i += 1
            st_date = end+datetime.timedelta(days=1)
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
        end_of_month = self.get_end_of_month(start)
        end = start
        c = rem
        rem -= 1
        for i in range(1, c):
            end = end+datetime.timedelta(days=1)
            rem -= 1
            if end == end_of_month:
                return end, rem, True
        return end, rem, False

    def sum_cube(self, st, end):
        """
        >>> c = Reporter(CubeFactSubscribedUsers, 'b7ff76fd-e078-483a-8318-040a92df7dc9')
        >>> c.sum_cube(datetime.datetime.strptime('2014-03-12', '%Y-%m-%d').date(),  datetime.datetime.strptime('2014-03-12', '%Y-%m-%d').date())
        1
        """
        self.cube = self.cube.filter(date__gte=st)
        self.cube = self.cube.filter(date__lte=end)
        total = self.cube.aggregate(total=Sum('total_new'), breakdown_pct=Sum('breakdown_pct'))
        total['total'] = 0 if total['total'] is None else total['total']
        total['breakdown_pct'] = 0 if total['breakdown_pct'] is None else total['breakdown_pct']
        return total

    def get_end_of_month(self, st_date):
        """
        >>> c = Reporter(CubeSubscriptionsDaily, 'b7ff76fd-e078-483a-8318-040a92df7dc9')
        >>> c.get_end_of_month(datetime.datetime.strptime('2016-02-29', '%Y-%m-%d').date())
        datetime.date(2016, 3, 31)
        >>> c.get_end_of_month(datetime.datetime.strptime('2014-02-28', '%Y-%m-%d').date())
        datetime.date(2014, 3, 31)
        >>> c.get_end_of_month(datetime.datetime.strptime('2014-01-25', '%Y-%m-%d').date())
        datetime.date(2014, 2, 25)
        >>> c.get_end_of_month(datetime.datetime.strptime('2014-03-25', '%Y-%m-%d').date())
        datetime.date(2014, 4, 25)
        >>> c.get_end_of_month(datetime.datetime.strptime('2014-03-31', '%Y-%m-%d').date())
        datetime.date(2014, 4, 30)
        >>> c.get_end_of_month(datetime.datetime.strptime('2014-02-11', '%Y-%m-%d').date())
        datetime.date(2014, 3, 11)
        >>> c.get_end_of_month(datetime.datetime.strptime('2014-01-31', '%Y-%m-%d').date())
        datetime.date(2014, 2, 28)

        """
        if st_date.month >= 12:
            month = 1
            year = st_date.year + 1
            return datetime.date(year, month, st_date.day)
        elif st_date.month == 1:
            if calendar.isleap(st_date.year):
                day = 29 if st_date.day > 29 else st_date.day
            else:
                day = 28 if st_date.day > 28 else st_date.day
            month = st_date.month + 1
            year = st_date.year
            end = datetime.date(year, month, day)
            return end
        elif st_date.month == 2:
            if st_date.day == 28 or st_date.day == 29:
                end = datetime.date(st_date.year, 3, 31)
                return end
            else:
                return datetime.date(st_date.year, st_date.month+1, st_date.day)
        if st_date.day == 31 or st_date.day == 30:
            day = calendar.monthrange(st_date.year, st_date.month+1)[1]
        else:
            day = st_date.day
        return datetime.date(st_date.year, st_date.month+1, day)


