from celery.task import task

from apps.events.aggregator import SERVICE_NAME
from apps.events.event_tools import parse_args_as_json

from apps.base.models import FactServicesAggregatorAggregation


@task()
@parse_args_as_json('{}.Aggregation'.format(SERVICE_NAME))
def aggregation(data):
    """
    Aggregator: Aggregation add

    asset_id
    asset_type
    unique_studio_item_id
    studio
    data_role
    definition
    language
    audio_channel
    client_id
    vendor
    file_name
    start_time
    end_time
    file_size
    checksum
    content_duration
    event_time
    """
    FactServicesAggregatorAggregation.create_fact(**data)