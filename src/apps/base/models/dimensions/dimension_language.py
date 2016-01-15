from django.db import models
from apps.base.models.dimensions.dimension import select_or_insert


class DimensionLanguage(models.Model):
    """
    DimensionLanguage

    Dim to filter down on languages within the reported data facts
    """
    iso_code = models.CharField(max_length=8, unique=True)

    class Meta:
        app_label = 'base'
        db_table = 'dim_language'

    @classmethod
    def insert(cls, **kwargs):
        return select_or_insert(cls, values={}, **kwargs)
