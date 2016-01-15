from django.db import models
from dimension import select_or_insert


class DimensionProcessingState(models.Model):

    processing_state = models.CharField(max_length=255)

    class Meta:
        app_label = 'base'
        db_table = 'dim_processing_state'

    @classmethod
    def insert(cls, **kwargs):
        return select_or_insert(cls, values={}, **kwargs)

