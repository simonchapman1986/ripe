from django.db import models
from apps.base.models.dimensions.dimension import select_or_insert


class DimensionTransactionType(models.Model):
    """
    DimensionTransactionType

    Dim to filter down on types of transactions we may recieve within the reported data facts
    """
    transaction_type = models.CharField(max_length=255, unique=True)

    class Meta:
        app_label = 'base'
        db_table = 'dim_transaction_type'

    @classmethod
    def insert(cls, **kwargs):
        return select_or_insert(cls, values={}, **kwargs)
