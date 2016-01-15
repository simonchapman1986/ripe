from django.db import models
from apps.base.models.dimensions.dimension import select_or_insert

recurring_subscription = -1
finished_subscription = 0


class DimensionSubscriptionType(models.Model):
    """
    (Deprecated)

    DimensionSubscriptionType

    Dim to filter down on definitions within the reported data facts

    - this is now legacy due to the window dimension. But remains util filtered out through the systems
    """
    period = models.CharField(max_length=25, null=True, default=None)
    recurrence = models.IntegerField(null=True, default=None)

    class Meta:
        app_label = 'base'
        db_table = 'dim_subscription_type'
        unique_together = ('period', 'recurrence')

    @classmethod
    def insert(cls, **kwargs):
        return select_or_insert(cls, values={}, **kwargs)
