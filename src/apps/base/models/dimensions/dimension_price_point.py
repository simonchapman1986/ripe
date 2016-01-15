from django.db import models
from dimension import insert_or_update


class DimensionPricePoint(models.Model):
    """
    DimensionPricePoint

    Dim to filter down on price points within the reported data facts
    This is ingested data that gives information about the pricing of a said report (i.e. subscription)
    """

    cms_price_point_id = models.IntegerField(null=True, blank=True)
    sale_type = models.CharField(max_length=10L, null=True, blank=True)
    definition_type = models.CharField(max_length=10L, null=True, blank=True)
    tier_name = models.CharField(max_length=30L, null=True, blank=True)
    tier_type = models.CharField(max_length=10L, null=True, blank=True)
    price = models.DecimalField(null=True, max_digits=11, decimal_places=2, blank=True)
    provider_share = models.DecimalField(null=True, max_digits=11, decimal_places=2, blank=True)
    provider_minimum = models.DecimalField(null=True, max_digits=11, decimal_places=2, blank=True)
    saffron_share = models.DecimalField(null=True, max_digits=11, decimal_places=2, blank=True)
    saffron_minimum = models.DecimalField(null=True, max_digits=11, decimal_places=2, blank=True)
    is_promotion = models.IntegerField(null=True, blank=True)

    class Meta:
        app_label = 'base'
        db_table = 'dim_price_point'

    @classmethod
    def insert(cls, update, cms_price_point_id, **values):
        return insert_or_update(cls,
                                update,
                                values=values,
                                cms_price_point_id=cms_price_point_id)