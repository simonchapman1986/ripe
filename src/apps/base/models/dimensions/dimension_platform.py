from django.db import models
from apps.base.models.dimensions.dimension import select_or_insert


class DimensionPlatform(models.Model):
    """
    DimensionDPlatform

    Dim to filter down on definitions within the reported data facts. Each dim is comprised of 3 unique together
    fields, the 'os' the 'name' and 'version'
    """
    os = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255, null=True)
    version = models.CharField(max_length=255, null=True)

    class Meta:
        app_label = 'base'
        db_table = 'dim_platform'
        unique_together = ("os", "name", "version")

    @classmethod
    def insert(cls, os, name, version):
        return select_or_insert(cls,
                                values={},
                                os=os,
                                name=name,
                                version=version)
