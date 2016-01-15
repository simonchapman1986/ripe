from django.db import models
from django_extensions.db.fields import UUIDField

from dimension import update_or_insert
from apps.base.models.dimensions.dimension_item_provider import DimensionItemProvider

from apps.flags.checks.item import item



import logging
log = logging.getLogger('reporting')

class DimensionItem(models.Model):
    """
    DimensionItem

    Dim to filter down on items within the reported data facts.

    Our Items hold relevant data that can be imperative to some of our reports. Ids that come in with our facts,
    generally do not hold this information so its very important the the information exists via the ingestion
    of item related events.

    Therefore we have our flagging system again in play here. Not upon insertion this time, as thats pointless
    as we are the dim. Instead here we have an added check class method, this can be used in facts that use this
    dimension to flag up if an item is missing, we can further improve on our flags to assert the data that exists
    for an item.
    """

    item_id = UUIDField(version=4)
    content_type = models.CharField(max_length=30L, blank=True, null=True)
    item_title = models.CharField(max_length=255L, blank=True, null=True)
    release_year = models.IntegerField(null=True, blank=True)
    item_runtime = models.CharField(max_length=8L, blank=True, null=True)
    item_duration = models.IntegerField(null=True, blank=True)
    item_provider = models.ForeignKey(DimensionItemProvider, null=True, blank=True)
    last_modified = models.DateTimeField(null=True, blank=True)

    class Meta:
        app_label = 'base'
        db_table = 'dim_item'

    @classmethod
    def check(cls, **kwargs):
        item_id = kwargs.get('item_id', None)
        if item_id:
            item(item_id=item_id, event_name='insert', cls=cls)

    @classmethod
    def insert(cls, item_id, **values):
        if item_id:
            cls.check(**{'item_id': item_id})
        return update_or_insert(cls,
                                values=values,
                                item_id=item_id)