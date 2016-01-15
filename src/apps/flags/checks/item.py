from apps.flags.report import register_flag
from apps.flags.report import DOES_NOT_EXIST


DESCRIPTION = 'Cannot Locate by Item ID ({}) in dim_items table'


def item(item_id, event_name, cls):
    """
    item

    to be used to check if an item exists, if it doesnt, we create a flag within the RIPE system
    """
    try:
        cls.objects.get(item_id=item_id)
    except cls.DoesNotExist:
        register_flag(
            type=DOES_NOT_EXIST,
            description=DESCRIPTION.format(item_id),
            event=event_name
        )
