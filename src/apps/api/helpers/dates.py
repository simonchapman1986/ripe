from string import digits, ascii_letters
from apps.api.exception import RipeApiException
from django.db.models import Sum
from django.db.models import Min
from django.db.models import Max
from django.db.models.base import ModelBase


import datetime
import logging
trace = logging.getLogger('trace')


def fail(name, legal_chars):
    message = u"The field '{}' may only contain characters from the set '{}'.".format(name, legal_chars)
    raise RipeApiException(
        *RipeApiException.CHARACTER_CHECK_FAILURE,
        debug_message=message
    )


def character_checker(*legal_character_lists):
    legal_chars = "".join(legal_character_lists)

    def checker(**fields):
        for name, value in fields.items():
            if value:
                for char in value:
                    if char not in legal_chars:
                        fail(name, legal_chars)
    return checker

def previous_report_date(start_date, end_date, period=None):
    """
    >>> previous_report_date('2013-01-01', '2013-01-30')
    1
    """
    start = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.datetime.strptime(end_date, '%Y-%m-%d')

    diff = abs((end - start).days)

    if period:
        if period=='monthly':
            new_start = monthdelta(start, -1)
        elif period=='weekly':
            new_start = start-datetime.timedelta(weeks=1)
        elif period=='daily':
            new_start = start-datetime.timedelta(days=1)
        else:
            raise RipeApiException(
                *RipeApiException.INCORRECT_PERIOD_PREVIOUS_REPORT,
                debug_message=u'Incorrect Period set for previous report date'
            )
    else:
        new_start = start-datetime.timedelta(days=diff)

    new_start = new_start.strftime("%Y-%m-%d")
    new_end = start.strftime("%Y-%m-%d")

    return new_start, new_end

def monthdelta(date, delta):
    """
    >>> date = datetime.datetime(2013, 01, 15)
    >>> monthdelta(date=date, delta=0)
    1
    """
    def date_inter(date, y, m, d):
        try:
            _date = date.replace(day=d,month=m, year=y)
        except ValueError:
            return date_inter(date, y, m, d-1)

        return _date

    m, y = (date.month+delta) % 12, date.year + ((date.month)+delta-1) // 12
    if not m: m = 12

    new_date = date_inter(date, y, m, date.day)

    return new_date

def month_end(date, d=31):
    """
    >>> date = datetime.datetime(2013, 01, 15)
    >>> month_end(date=date)
    datetime.datetime(2013, 1, 31, 0, 0)
    >>> date = datetime.datetime(2013, 02, 15)
    >>> month_end(date=date)
    datetime.datetime(2013, 2, 28, 0, 0)
    """
    try:
        _date = date.replace(day=d)
    except ValueError:
        return month_end(date, d-1)

    return _date


def get_date_range(start, end, cube=None, interval=None):
    # trace.info('{} {} inter: {}'.format(start, end, cube, interval))
    if not cube or not isinstance(cube, ModelBase):
        message = u"Incorrect cube type: '{}'.".format(type(cube))
        raise RipeApiException(
            *RipeApiException.BAD_CUBE,
            debug_message=message
        )

    if start == end == 'all':
        start = cube.objects.aggregate(Min('date'))['date__min']
        #todo could change to current date later
        end = cube.objects.aggregate(Max('date'))['date__max']
    elif start == 'all' and end != 'all':
        start = cube.objects.aggregate(Min('date'))['date__min']
    elif end == 'all' and start != 'all':
        #todo could change to current date later
        end = cube.objects.aggregate(Max('date'))['date__max']

    #cal the date range based on interval
    dt_range = []
    if interval == 'daily':
        try:
            dt_range = [(start+datetime.timedelta(days=i), start+datetime.timedelta(days=i)) for i in range((end-start).days+1)]
        except Exception:
            trace.exception('\n\n')
    elif interval == 'total':
        dt_range = []
    elif interval == 'weekly':
        if (end-start).days <= 6:
            dt_range.append((start, end))
        else:
            seven = datetime.timedelta(days=7)
            wk_start = start
            wk_end = start+datetime.timedelta(days=6)
            dt_range.append((wk_start, wk_end))
            while wk_end < end:
                wk_start = wk_start + seven
                wk_end = wk_end + seven
                if wk_start <= end < wk_end:
                    wk_end = end
                dt_range.append((wk_start, wk_end))
    elif interval == 'monthly':
        mth_end = month_end(start)
        dt_range.append((start, mth_end))
        while mth_end < end:
            mth_start = mth_end+datetime.timedelta(days=1)
            mth_end = month_end(mth_start)
            dt_range.append((mth_start, mth_end))
    # trace.info('s: {} e: {} range: {}'.format(start, end, dt_range))
    return start, end, dt_range



    ALPHANUMERICS = character_checker(digits, ascii_letters)
    ALPHANUMERICS_PLUS = character_checker(digits, ascii_letters, "-_")
    DATE_TIME = character_checker(digits, "-")