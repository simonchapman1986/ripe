from celery.task import task

from apps.events.heartbeat import SERVICE_NAME
from apps.events.event_tools import parse_args_as_json

from apps.base.models import FactServicesHeartbeatPlay


@task()
@parse_args_as_json('{}.Plays'.format(SERVICE_NAME))
def plays(data):
    """
    Heartbeat: Plays event injection (inclusive for buffer and init events paired)

    ip_address_chain [x, y, z]
    item_id
    client_id
    device_id
    status
    internal_user_id
    external_user_id
    position
    bitrate
    buffer_events [a, b, c] (optional)
    init_length (optional)
    init_licensed (optional)
    date
    """
    FactServicesHeartbeatPlay.create_fact(**data)