from celery.task import task

from apps.events.backstage import SERVICE_NAME
from apps.events.event_tools import parse_args_as_json

from apps.base.models import FactServicesBackstageAssetMatch


@task()
@parse_args_as_json('{}.ContentAssetMatch'.format(SERVICE_NAME))
def asset_match(data):
    """
    client_id
    item_id
    data_role
    definition
    processing_state
    territory
    asset_id
    asset_type
    provider_item_id
    provider (name)
    delivery_date
    spec_name
    file_size
    duration
    used_asset_ids (list)
    languages (list)
    event_time
    """
    FactServicesBackstageAssetMatch.create_fact(**data)
