from django.db import models
from dimension import select_or_insert


class DimensionStudio(models.Model):
    """
    DimensionStudio

    """

    name = models.CharField(max_length=255)

    class Meta:
        app_label = 'base'
        db_table = 'dim_studio'

    @classmethod
    def insert(cls, **kwargs):
        return select_or_insert(cls, values={}, **kwargs)
