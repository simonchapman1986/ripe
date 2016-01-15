from django.db import models
from apps.base.models.dimensions.dimension import select_or_insert


class DimensionRetailModel(models.Model):
    """
    DimensionRetailModel

    Dim to filter down on retail models within the reported data facts
    """
    model = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        app_label = 'base'
        db_table = 'dim_retail_model'

    @classmethod
    def insert(cls, **kwargs):
        return select_or_insert(cls, values={}, **kwargs)
