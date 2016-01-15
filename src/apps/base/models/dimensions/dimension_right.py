from django.db import models
from apps.base.models.dimensions.dimension import select_or_insert

from apps.flags.checks.right import right

import logging
log = logging.getLogger('reporting')


class DimensionRight(models.Model):
    """
    DimensionRight

    Dim to filter down on usage rights within the reported data facts

    to be revised with more information from locker
    """
    right_id = models.CharField(max_length=255, unique=True)

    class Meta:
        app_label = 'base'
        db_table = 'dim_right'

    @classmethod
    def insert(cls, **kwargs):
        right(right_id=kwargs['right_id'], event_name='insert', cls=cls)
        return select_or_insert(cls, values={}, **kwargs)
