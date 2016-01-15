from apps.flags.report import register_flag
from apps.flags.report import DOES_NOT_EXIST

from apps.base.models.utilities.client import Clients


DESCRIPTION = 'Cannot Locate by Client ID ({}) in clients table'


def client(client_id, event_name):
    """
    client

    used to assert whether the client does indeed exist in our ingested clients table, if not this is a potential
    issue and it must be flagged
    """
    try:
        Clients.objects.get(id=client_id)
    except Clients.DoesNotExist:
        register_flag(
            type=DOES_NOT_EXIST,
            description=DESCRIPTION.format(client_id),
            event=event_name
        )
