
from django.conf import settings
from django.http import HttpResponse
from os.path import join, basename
from paramiko import Transport, SFTPClient
from apps.base.models.utilities.client import Clients
import logging



logger = logging.getLogger('reporting')
trace = logging.getLogger('trace')


class BuildCsv(object):

    def __init__(self):
        self._json = None

    def input_json_structure(self, json):
        self._json = json

    def build(self):

        headers = ','.join(
            settings.RIPE_RESPONSE['CSV_HEADERS']
        )
        curr_report = self._json.get(
            self._report_name, None
        ).get(
            'current_report', None
        )

        #TODO for file-name creation
        attributes = curr_report.pop('attributes', None)
        row_fields = list(settings.RIPE_RESPONSE['CSV_ROW_FIELD_INDEX'])
        values = ''
        req_headers = list(settings.RIPE_RESPONSE['CSV_HEADERS'])
        for k, val in curr_report.iteritems():
            row = {str(req_headers[i]): '' for i in row_fields}
            for i in row:
                row[i] = val[i]
            groups = False
            for k, v in val.iteritems():
                if k not in headers:
                    groups = True
                    t = dict(row)
                    t.update(v)
                    t['group'] = k
                    values = values + '\n{}'.format(
                        ','.join(
                            [str(t[h]) for h in settings.RIPE_RESPONSE['CSV_HEADERS']]
                        )
                    )
                elif k not in row:
                    row[k] = val[k]
            if not groups:
                if not values:
                    del req_headers[req_headers.index('group')]
                values = values + '\n{}'.format(','.join(
                    [str(row[h]) for h in req_headers]
                ))
        headers = ','.join(
            [str(h).title() for h in req_headers]
        )
        # join
        self._data = headers+values
        # return

        return self._data

    def response(self, name):
        # create response object for CSV
        resp = HttpResponse(self._data, content_type='text/csv')
        resp['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(name)

        return resp

    def save_local(self, absolute_filename):
        """
        Write the given report sections to the given file, in CSV format.

        report_sections is a list of pairs, the first item in the pair is the
        header, the second item in the pair is a list of rows.
        """
        output = open(absolute_filename, 'w')
        output.write(self._data)

    def upload_report_to_sftp(self, client_id, report_date, absolute_filename):
        """
        Upload the given file, using SFTP, to the configured FTP server. The
        file should be uploaded to the appropriate directory for the specified
        client and the date of the report.
        """
        try:
            client = Clients.objects.get(id=client_id)
        except Clients.DoesNotExist:
            logger.exception(u'No configuration for client {0}.'.format(client_id))
            raise

        filename = basename(absolute_filename)
        base_folder, env_folder, year_folder, month_folder = self._get_sftp_dirs(client, report_date)

        try:
            logger.debug(u'SFTP logging on to {0} as {1}'.format(settings.SFTP_SERVER, settings.SFTP_USERNAME))
            transport = Transport((settings.SFTP_SERVER, settings.SFTP_PORT))
            transport.connect(username=settings.SFTP_USERNAME, password=settings.SFTP_PASSWORD)
            sftp = SFTPClient.from_transport(transport)

            logger.debug(u'SFTP dir {0}/{1}/{2}/{3}'.format(base_folder, env_folder, year_folder, month_folder))
            sftp.chdir(base_folder)
            self._make_or_change_sftp_dir(sftp, env_folder)
            self._make_or_change_sftp_dir(sftp, year_folder)
            self._make_or_change_sftp_dir(sftp, month_folder)

            logger.debug(u'SFTP uploading {0}'.format(filename))
            sftp.put(absolute_filename, filename)
        except Exception:
            logger.exception(u'Unrecoverable exception during SFTP upload process.')
            raise
        finally:
            logger.debug(u'SFTP logging off')

            try:
                sftp.close()
            except Exception:
                logger.exception(u'SFTP exception while closing SFTP session.')

            try:
                transport.close()
            except Exception:
                logger.exception(u'SFTP exception while closing SSH connection.')

    @staticmethod
    def _get_sftp_dirs(client, report_date):
        """
        Returns the four levels of directory names needed for SFTP
        upload: base, environment, year, month.
        """
        ftp_client_dir = client.ftp_client_dir
        if ftp_client_dir == '':
            ftp_client_dir = getattr(settings, 'DEFAULT_SFTP_LOCATION', 'default')
            logger.exception(u'No FTP configuration for client {} using default value.'.format(client.name))

        base_folder = join('/',
                           getattr(settings, 'SFTP_HOMEDIR', 'home'),
                           ftp_client_dir,
                           getattr(settings, 'SFTP_REPORTSDIR', 'reports'))
        env_folder = str(getattr(settings, 'FTP_ENV_FOLDER', 'dev') or 'dev').lower()
        year_folder, month_folder, _ = report_date.split('-')
        return base_folder, env_folder, year_folder, month_folder

    @staticmethod
    def _make_or_change_sftp_dir(sftp, dirname):
        """
        Try to change to the given directory on the given SFTP connection.
        If that fails, make the directory and try changing directory again.
        """
        try:
            sftp.chdir(dirname)
        except IOError:
            sftp.mkdir(dirname)
            sftp.chdir(dirname)