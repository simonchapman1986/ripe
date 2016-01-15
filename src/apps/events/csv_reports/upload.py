from datetime import timedelta
from celery.task import periodic_task
from celery.task import task
from django.conf import settings
from apps.reporting.csv_reports.csv_generator import CSVgenerator
from apps.base.models.dimensions.dimension_client import DimensionClient
from apps.events.csv_reports import upload_tasks


import logging
log = logging.getLogger('reporting')


@task()
def upload_report():

    #TODO update REPORT_UPLOAD_INTERVAL after sftp credentials available and QA.

    report_names = getattr(settings, 'UPLOAD_REPORTS', None)

    if not report_names:
        log.info('Unable to upload reports. Required Config settings not found.')
        raise Exception('Unable to upload reports. Required Config settings not found.')

    for report in report_names:
        upload_tasks.upload_report_for_all_clients.delay(report)

    # get all clients in ripe.
    clients = DimensionClient.objects.all()
    for c in clients:
        for report in report_names:
            upload_tasks.upload_report_for_client.delay(report, c)


