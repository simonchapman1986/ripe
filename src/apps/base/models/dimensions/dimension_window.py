from django.db import models
from apps.base.models.dimensions.dimension import select_or_insert
from apps.base.models.dimensions.dimension_item import DimensionItem
from apps.base.models.dimensions.dimension_product import DimensionProduct
from apps.base.models.dimensions.dimension_right import DimensionRight

import logging
log = logging.getLogger('reporting')

class DimensionWindow(models.Model):
    """
    DimensionWindow

    (supersedes Dim Subscription Type)

    Dim to filter down on a window for a given, purchase, or subscription etc within the reported data facts
    As the data within the window is linked towards other dims, we check that data exists, and also add it across
    to keep things sane across the board.
    """
    window_id = models.CharField(max_length=255, null=True)
    item = models.ForeignKey(DimensionItem, null=True)
    product = models.ForeignKey(DimensionProduct, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    pricing_id = models.CharField(max_length=255, null=True)
    usage_right = models.ForeignKey(DimensionRight, null=True)
    tier = models.CharField(max_length=255, null=True)
    deleted = models.DateField(blank=True, null=True)
    window_type = models.CharField(max_length=255, null=True)
    on_going = models.BooleanField(default=False)
    repeat_count = models.IntegerField(max_length=10, default=0)
    auto_upgrade = models.BooleanField(default=False)
    allow_repurchase = models.BooleanField(default=False)
    apple_product_id = models.CharField(max_length=255, null=True)


    class Meta:
        app_label = 'base'
        db_table = 'dim_window'

    @classmethod
    def insert(cls, **kwargs):

        # clear out empty items
        kwargs = {key: value for key, value in kwargs.items() if value is not u''}

        if kwargs['item']:
            DimensionItem.check(**{'item_id': kwargs['item'].item_id})

        return select_or_insert(cls, values={}, **kwargs)
