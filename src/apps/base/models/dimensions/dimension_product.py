from django.db import models
from apps.base.models.dimensions.dimension import select_or_insert


class DimensionProduct(models.Model):
    """
    DimensionProduct

    Dim to filter down on products within the reported data facts
    """
    product_id = models.CharField(max_length=255, unique=True)

    class Meta:
        app_label = 'base'
        db_table = 'dim_product'

    @classmethod
    def insert(cls, **kwargs):
        return select_or_insert(cls, values={}, **kwargs)
