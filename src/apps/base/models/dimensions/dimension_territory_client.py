from django.db import models
from django_extensions.db.fields import UUIDField
from dimension import insert_or_update


class DimensionTerritoryClient(models.Model):
    """
    DimensionTerritoryClient

    Dim to filter down on territories for a client within the reported data facts
    """

    client_id = UUIDField(max_length=36L, blank=True, null=True)
    client_name = models.CharField(max_length=100L, blank=True, null=True)
    territory_id = models.IntegerField(blank=True, null=True)
    territory_name = models.CharField(max_length=20L, blank=True, null=True)
    currency_code = models.CharField(max_length=3L, blank=True, null=True)
    currency_name = models.CharField(max_length=100L, blank=True, null=True)
    country_code = models.CharField(max_length=3L, blank=True, null=True)
    country_name = models.CharField(max_length=128L, blank=True, null=True)
    region_code = models.CharField(max_length=3L, blank=True, null=True)
    region_name = models.CharField(max_length=100L, blank=True, null=True)
    territory_timezone = models.CharField(max_length=63L, blank=True, null=True)

    class Meta:
        app_label = 'base'
        db_table = 'dim_territory_client'

    @classmethod
    def insert(cls, update, client_id, territory_name, **values):
        return insert_or_update(cls,
                                update,
                                values=values,
                                client_id=client_id,
                                territory_name=territory_name)

