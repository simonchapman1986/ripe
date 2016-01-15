import logging

from django.conf import settings
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET

from apps.base.models import Clients
from saffron.api.response import ApiSuccessHttpResponse
from sd_api_utils import health_checks
from apps.api.views.v1 import get_celery_worker_status

logger = logging.getLogger(__name__)


@require_GET
@never_cache
def check_instance(request, *args, **kwargs):
    """#apidoco
        method: GET
    """
    health = health_checks.check_instance(model=Clients)

    if not get_celery_worker_status():
        health['celery_ok'] = False
        health['ok'] = False
    else:
        health['celery_ok'] = True

    if not health['ok']:
        logger.error(u'Health check failed: {}'.format(health))
        return ApiSuccessHttpResponse(health, http_code=500)
    else:
        return ApiSuccessHttpResponse(health)


@require_GET
@never_cache
def monitor_instance(request, *args, **kwargs):
    """#apidoco
        method: GET
    """
    apis = {
        'service_manager': settings.SERVICE_MANAGER_INTERNAL_URI + '/api/v1/check_instance/',
    }

    for client in Clients.objects.all():
        if client.auth_service_url:
            if '/api/v1' in client.auth_service_url:
                apis['auth-' + client.name] = client.auth_service_url + '/check_instance/'
            else:
                apis['auth-' + client.name] = client.auth_service_url + '/api/v1/check_instance/'

    health = health_checks.monitor_instance(model=Clients, apis=apis)

    if not health['ok']:
        return ApiSuccessHttpResponse(health, http_code=500)
    else:
        return ApiSuccessHttpResponse(health)
