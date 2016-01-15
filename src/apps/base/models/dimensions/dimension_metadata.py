from django.db import models
from django_extensions.db.fields import UUIDField

from apps.base.models.dimensions.dimension import select_or_insert


class DimensionMetadata(models.Model):
    """
    DimensionMetadata

    Dim to filter down on metadata within the reported data facts. This is a spinoff of the metadata fact.
    This allows us to ingest our metadata items, then use the dim to filter down on other incoming events
    """
    metadata_id = UUIDField(version=4, unique=True)

    class Meta:
        app_label = 'base'
        db_table = 'dim_metadata'

    @classmethod
    def insert(cls, **kwargs):
        return select_or_insert(cls, values={}, **kwargs)
