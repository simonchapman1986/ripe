from django.db import models
from dimension import select_or_insert


class DimensionAccount(models.Model):
    """
    DimensionAccount

    Dim to filter down on accounts within the reported data facts
    """

    account_id = models.CharField(max_length=255, blank=True, null=True, default='')
    account_created = models.DateTimeField(null=True, blank=True)

    class Meta:
        app_label = 'base'
        db_table = 'dim_account'

    @classmethod
    def insert(cls, **kwargs):
        return select_or_insert(cls, values={}, **kwargs)
