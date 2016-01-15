from django.db import models
from apps.base.models.dimensions.dimension import select_or_insert


class DimensionJobManager(models.Model):
    """
    DimensionJobManager

    Dim to filter down on job managers within the reported data facts
    """

    job_manager_id = models.CharField(max_length=255, unique=True)

    class Meta:
        app_label = 'base'
        db_table = 'dim_job_manager'

    @classmethod
    def insert(cls, **kwargs):
        return select_or_insert(cls, values={}, **kwargs)
