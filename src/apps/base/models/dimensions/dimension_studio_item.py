from django.db import models
from dimension import select_or_insert


class DimensionStudioItem(models.Model):
    """
    DimensionStudioItem

    """

    unique_studio_item_id = models.CharField(max_length=255, default='')

    class Meta:
        app_label = 'base'
        db_table = 'dim_studio_item'

    @classmethod
    def insert(cls, **kwargs):
        return select_or_insert(cls, values={}, **kwargs)
