from django.db import models
from django_extensions.db.fields import UUIDField

from apps.base.models.dimensions.dimension_utc_date import DimensionUTCDate

from uuid import uuid4

import datetime
import json
import logging

logger = logging.getLogger('reporting')


class Log(models.Model):
    """
    Flags

    we store our flags against the utc_date_event - we do this because we will be able to generate reports based
    upon our flagged issues to show ongoing problems within RIPE or indeed NEXUS as a whole.
    """
    id = UUIDField(version=4, primary_key=True)
    packet = models.TextField()
    event = models.CharField(max_length=128)
    completed = models.BooleanField(default=False)
    event_utc_date = models.ForeignKey(DimensionUTCDate)
    event_utc_datetime = models.DateTimeField()

    class Meta:
        app_label = 'Log'
        db_table = 'event_log'

    @classmethod
    def create_flag(cls, event_name, packet, **kwargs):
        # This code only happens if the objects is
        # not in the database yet. Otherwise it would
        # have pk
        # we are going to set some datetime params - we may need to create a report
        # on this data later and this will be useful information to correlate against
        kwargs['id'] = str(uuid4())
        kwargs['event'] = event_name
        kwargs['packet'] = json.dumps(packet)
        kwargs['event_utc_datetime'] = datetime.datetime.utcnow()
        kwargs['event_utc_date'] = DimensionUTCDate.date_from_datetime(kwargs['event_utc_datetime'])

        cls.objects.create(**kwargs)
