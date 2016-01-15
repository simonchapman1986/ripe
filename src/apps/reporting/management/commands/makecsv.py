from django.core.management.base import BaseCommand
from apps.reporting.csv_reports.csv_generator import CSVgenerator
from apps.events.csv_reports import upload


import logging
log = logging.getLogger('reporting')


class Command(BaseCommand):

    help = 'Creates CSV for a report.'

    def handle(self, *args, **options):

        self.stdout.write(u'Uploading reports...')
        try:
            upload.upload_report.delay()
        except Exception:
            log.exception('')
            self.stdout.write(u'Exception occurred while uploading reports.')

