from celery.task import task
from apps.reporting.csv_reports.csv_generator import CSVgenerator
import logging
log = logging.getLogger('reporting')


@task()
def upload_report_for_client(report_type, client):

    gen = CSVgenerator(report_type=report_type, client_id=client.client_id, args=None)
    try:
        gen.generate()
    except Exception:
        log.exception('Exception occurred while generating report for client-ID {} :: ripe-client-ID {}'.format(
            client.client_id, client.id
        )
        )


@task()
def upload_report_for_all_clients(report_type):

    log.info('Uploading aggregated {} report for all clients.'.format(report_type))
    gen = CSVgenerator(report_type=report_type, args=None)
    gen.generate()


