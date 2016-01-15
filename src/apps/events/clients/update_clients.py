import logging
from datetime import timedelta

from celery.task import periodic_task
from django.conf import settings

from sd_api_clients.service_manager.v1.service_manager_api_client import SimpleServiceManagerApiClient

from apps.base.models.utilities.client import Clients
from apps.base.models.utilities.config import Config

from apps.events.clients import SERVICE_NAME


logger = logging.getLogger('reporting')


@periodic_task(run_every=timedelta(seconds=settings.CLIENT_UPDATE_TIMEDELTA))
def update_clients():
    """
    update_clients

    the update clients event exists as a period task run every (x) (please see the settings) seconds

    The task event then ingests the client information within NEXUS that the service will need for its reported
    clients.
    """
    logger.info('Starting: {0}'.format(SERVICE_NAME))
    access_key = Config.get_config(Config.ACCESS_KEY)
    access_secret = Config.get_config(Config.ACCESS_SECRET)

    uri = settings.SERVICE_MANAGER_INTERNAL_URI
    service_manager = SimpleServiceManagerApiClient(uri, access_key, access_secret)
    clients_data = service_manager.get_clients()

    for client_data in clients_data:
        try:
            client = Clients.objects.get(id=client_data.get('id'))
            logger.info('Updating client: {0}'.format(client_data.get('id')))
        except Clients.DoesNotExist:
            client = Clients()
            logger.info('Creating client: {0}'.format(client_data.get('id')))

        client.id = client_data.get('id', client.id)
        client.name = client_data.get('name', client.name)
        client.description = client_data.get('description', client.description)

        config = client_data.get('config', {})
        client.ftp_client_dir = config.get('ftp_client_dir', client.ftp_client_dir)

        client.save()

    logger.info('Completed: {0}'.format(SERVICE_NAME))

    return True