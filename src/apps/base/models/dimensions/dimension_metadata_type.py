from django.db import models
from dimension import select_or_insert


class DimensionMetadataType(models.Model):
    """
    DimensionMetadataType

    Dim to filter down on metadata types within the reported data facts
    """
    type = models.CharField(max_length=255, unique=True)

    class Meta:
        app_label = 'base'
        db_table = 'dim_metadata_type'

    @classmethod
    def insert(cls, **kwargs):
        return select_or_insert(cls, values={}, **kwargs)
