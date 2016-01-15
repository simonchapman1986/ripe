from django.db import models
from apps.base.models.dimensions.dimension import select_or_insert


class DimensionVendor(models.Model):
    """
    DimensionVender

    Dim to filter down on vendors within the reported data facts
    """
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        app_label = 'base'
        db_table = 'dim_vendor'

    @classmethod
    def insert(cls, **kwargs):
        return select_or_insert(cls, values={}, **kwargs)
