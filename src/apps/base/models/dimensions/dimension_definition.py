from django.db import models
from apps.base.models.dimensions.dimension import select_or_insert


class DimensionDefinition(models.Model):
    """
    DimensionDefinition

    Dim to filter down on definitions within the reported data facts
    """
    definition = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        app_label = 'base'
        db_table = 'dim_definition'

    @classmethod
    def insert(cls, **kwargs):
        return select_or_insert(cls, values={}, **kwargs)
