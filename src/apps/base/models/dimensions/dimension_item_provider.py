from django.db import models
from dimension import insert_or_update


class DimensionItemProvider(models.Model):
    """
    DimensionDItemProvider

    Dim to filter down on item providers within the reported data facts
    """

    # provider_id = models.IntegerField(unique=True, null=True, blank=True)
    # provider_name = models.CharField(max_length=128L, unique=True, blank=True, null=True)

    # datatype according to content-storage wiki.
    provider_id = models.CharField(max_length=128L, unique=True, blank=True, null=True)
    provider_name = models.CharField(max_length=128L, unique=True, blank=True, null=True)


    class Meta:
        app_label = 'base'
        db_table = 'dim_item_provider'

    @classmethod
    def insert(cls, update, provider_id, **values):
        return insert_or_update(cls,
                                update,
                                values=values,
                                provider_id=provider_id)
