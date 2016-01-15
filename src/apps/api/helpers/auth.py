import logging

from apps.reporting.tasks import update_services
from apps.reporting.models.service import Service

logger = logging.getLogger(__name__)


def get_secret_by_access_key(access_key):
    secret = Service.get_secret_by_access_key(access_key)
    if secret:
        return secret

    update_services()

    secret = Service.get_secret_by_access_key(access_key)
    if secret:
        return secret
    else:
        logger.debug('Service not found by access key: {0}'.format(access_key))
        return None
    return None
