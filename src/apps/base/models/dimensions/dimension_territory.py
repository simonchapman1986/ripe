from django.db import models
from apps.base.models.dimensions.dimension import select_or_insert


class DimensionTerritory(models.Model):
    """
    DimensionTerritory

    Dim to filter down on territories within the reported data facts
    """
    code = models.CharField(max_length=10, unique=True)

    class Meta:
        app_label = 'base'
        db_table = 'dim_territory'

    @classmethod
    def insert(cls, **kwargs):
        return select_or_insert(cls, values={}, **kwargs)
