import logging
from datetime import timedelta

from celery.task import periodic_task
from django.conf import settings

from sd_api_clients.service_manager.v1.service_manager_api_client import SimpleServiceManagerApiClient

from apps.base.models.utilities.service import Service
from apps.base.models.utilities.config import Config

from apps.events.services import SERVICE_NAME


logger = logging.getLogger('reporting')


@periodic_task(run_every=timedelta(seconds=settings.SERVICE_UPDATE_TIMEDELTA))
def update_services():
    """
    update_services

    the update services event exists as a period task run every (x) (please see the settings) seconds

    The task event then ingests the service information within NEXUS
    """
    logger.info('Starting: {0}'.format(SERVICE_NAME))
    access_key = Config.get_config(Config.ACCESS_KEY)
    access_secret = Config.get_config(Config.ACCESS_SECRET)

    uri = settings.SERVICE_MANAGER_INTERNAL_URI
    service_manager = SimpleServiceManagerApiClient(uri, access_key, access_secret)
    services_data = service_manager.get_my_services()

    for service_data in services_data:
        service, created = Service.objects.get_or_create(uuid=service_data.get('id'))
        logger.info('{0} service: {1}'.format('Creating' if created else 'Updating', service_data.get('id')))

        service.uuid = service_data.get('id', service.uuid)
        service.access_key = service_data.get('access_key', service.access_key)
        service.access_secret = service_data.get('access_secret', service.access_secret)
        service.name = service_data.get('name', service.name)

        service.save()

    logger.info('Completed: {0}'.format(SERVICE_NAME))

    return True