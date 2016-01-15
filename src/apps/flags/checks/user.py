from apps.flags.report import register_flag
from apps.flags.report import MISSING_DATA


def missing_user_id(event_name, description):
    """
    missing_user_id

    in the event that a user is yet to exist, we must flag this error accordingly as this is not a create user event.
    """
    register_flag(
        type=MISSING_DATA,
        description=description,
        event=event_name
    )
