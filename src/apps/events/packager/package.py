from celery.task import task

from apps.events.packager import SERVICE_NAME
from apps.events.event_tools import parse_args_as_json

from apps.base.models import FactServicesPackagerPackage


@task()
@parse_args_as_json('{}.Metadata'.format(SERVICE_NAME))
def package(data):
    """
    Packager: Package add

    job_manager_id
    item_id
    start_time
    end_time
    profile
    asset_ids []
    event_time
    """
    FactServicesPackagerPackage.create_fact(**data)