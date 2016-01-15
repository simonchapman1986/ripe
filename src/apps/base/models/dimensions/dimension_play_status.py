from django.db import models


class DimensionPlayStatus(models.Model):
    """
    DimensionSubscriptionStatus

    Dim to filter down on a subscriptions status within the reported data facts
    The incoming information is as an integer, however we translate this into its meaning as a description
    """
    status = models.CharField(max_length=20, default='unknown', unique=True)

    class Meta:
        app_label = 'base'
        db_table = 'dim_play_status'


    @classmethod
    def insert(cls, status):
        return DimensionPlayStatus.objects.get_or_create(status=status)
