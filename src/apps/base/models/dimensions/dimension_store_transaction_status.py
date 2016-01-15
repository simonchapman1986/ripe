from django.db import models
from apps.base.models.dimensions.dimension import select_or_insert


class DimensionStoreTransactionStatus(models.Model):
    """
    DimensionStoreTransactionStatus

    Dim to filter down on store transaction status within the reported data facts
    We use the predefined rule set on the incoming numerical values to determine the meaning
    """
    description = models.CharField(max_length=20, default='pending')

    class Meta:
        app_label = 'base'
        db_table = 'dim_store_transaction_status'


    @classmethod
    def insert(cls, status):
        return select_or_insert(cls, values={}, description=status)