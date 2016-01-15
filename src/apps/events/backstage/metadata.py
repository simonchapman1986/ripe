from celery.task import task

from apps.events.backstage import SERVICE_NAME
from apps.events.event_tools import parse_args_as_json

from apps.base.models import FactServicesBackstageItemMetadata


@task()
@parse_args_as_json('{}.Metadata'.format(SERVICE_NAME))
def metadata(data):
    """
    Backstage: Metadata updates/adds/changes etc

    metadata_id
    version
    provider_id
    provider_name
    primary_language
    vendor
    country_of_origin_iso
    type
    item_id
    title
    copyright_cline
    isan
    eidr
    release_date
    production_company
    release_year
    short_synopsis
    medium_synopsis
    long_synopsis
    runtime
    episode_number
    season
    show_title
    created
    modified
    original_url
    ultraviolet
    event_time
    """
    FactServicesBackstageItemMetadata.create_fact(**data)