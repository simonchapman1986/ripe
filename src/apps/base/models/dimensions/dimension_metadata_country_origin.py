from django.db import models
from apps.base.models.dimensions.dimension import select_or_insert


class DimensionCountryCode(models.Model):
    """
    DimensionCountryCode

    Dim to filter down on metadata country codes within the reported data facts
    """
    iso_code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        app_label = 'base'
        db_table = 'dim_metadata_country_code'

    @classmethod
    def insert(cls, **kwargs):
        return select_or_insert(cls, values={}, **kwargs)
