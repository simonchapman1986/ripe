from isodate import parse_date
from django.db import models


class DimensionUTCDate(models.Model):
    """
    DimensionUTCDate

    Dim to filter down on dates, days, months, years, and quarters etc within the reported data facts.

    Very useful and critical to the workings of the reporting system
    """
    date = models.DateField()
    year = models.SmallIntegerField()
    month = models.SmallIntegerField()
    day = models.SmallIntegerField()
    day_of_week = models.IntegerField()
    day_name = models.CharField(max_length=9)
    week_of_year = models.SmallIntegerField()
    quarter = models.SmallIntegerField()

    class Meta:
        app_label = 'base'
        db_table = 'dim_utc_date'

    @classmethod
    def date_from_datetime(cls, datetime):
        try:
            date = parse_date(datetime)
        except TypeError:
            date = datetime

        return DimensionUTCDate.objects.get(date=date)
