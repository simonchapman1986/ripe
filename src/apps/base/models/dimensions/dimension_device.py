from django.db import models
from django_extensions.db.fields import UUIDField
from apps.base.models.dimensions.dimension import select_or_insert


class DimensionDevice(models.Model):
    """
    DimensionDevice

    Dim to filter down on devices within the reported data facts
    """
    device_id = UUIDField(version=4, unique=True)
    make = models.CharField(max_length=255, blank=True, null=True, default='')
    model = models.CharField(max_length=255, blank=True, null=True, default='')
    os = models.CharField(max_length=255, blank=True, null=True, default='')
    os_version = models.CharField(max_length=255, blank=True, null=True, default='')

    class Meta:
        app_label = 'base'
        db_table = 'dim_device'
        unique_together = ("os", "make", "model", "os_version")

    @classmethod
    def insert(cls, **kwargs):
        return select_or_insert(cls, values={}, **kwargs)
