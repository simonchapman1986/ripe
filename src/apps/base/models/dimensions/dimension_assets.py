from django.db import models
from apps.base.models.dimensions.dimension import select_or_insert


class DimensionAssets(models.Model):
    """
    DimensionAssets

    Dim to filter down on assets within the reported data facts
    """
    asset_id = models.CharField(max_length=255, unique=True)
    type = models.CharField(max_length=255)

    class Meta:
        app_label = 'base'
        db_table = 'dim_assets'

    @classmethod
    def insert(cls, **kwargs):
        return select_or_insert(cls, values={}, **kwargs)
