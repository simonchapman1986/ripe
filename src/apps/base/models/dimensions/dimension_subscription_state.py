from django.db import models


class DimensionSubscriptionState(models.Model):
    """
    DimensionSubscriptionState

    Dim to filter down on a subscriptions state within the reported data facts
    """
    state = models.CharField(max_length=255, default='unknown', unique=True)

    class Meta:
        app_label = 'base'
        db_table = 'dim_subscription_state'
