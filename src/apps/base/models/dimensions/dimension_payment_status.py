from django.db import models
from dimension import select_or_insert


class DimensionPaymentStatus(models.Model):
    """
    DimensionPaymentStatus

    Dim to filter down on payments status within the reported data facts
    """
    status = models.CharField(max_length=128, unique=True)

    class Meta:
        app_label = 'base'
        db_table = 'dim_payment_status'

    @classmethod
    def insert(cls, **kwargs):
        return select_or_insert(cls, values={}, **kwargs)
