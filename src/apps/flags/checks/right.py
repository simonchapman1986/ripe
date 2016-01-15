from apps.flags.report import register_flag
from apps.flags.report import DOES_NOT_EXIST


DESCRIPTION = 'Cannot Locate by Right ID ({}) in dim_right table'


def right(right_id, event_name, cls):
    """
    right

    usage rights are supposed to be ingested by the locker events. If a usage right is yet to exist we
    flag this up.
    """
    try:
        cls.objects.get(right_id=right_id)
    except cls.DoesNotExist:
        register_flag(
            type=DOES_NOT_EXIST,
            description=DESCRIPTION.format(right_id),
            event=event_name
        )
