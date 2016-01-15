from apps.cubes.models.daily.registrations import CubeRegistrationsDaily
from apps.cubes.models.daily.subscriptions import CubeSubscriptionsDaily
from apps.cubes.models.daily.subscription_revenue import CubeSubscriptionRevenueDaily
from datetime import datetime
from datetime import timedelta
from apps.api.helpers.dates import get_date_range
from apps.reporting.utils.build_csv import BuildCsv
from django.conf import settings
from os.path import join
from os.path import abspath
from os.path import dirname
from os.path import split
import csv
import uuid
from apps.reporting.csv_reports.csv_config import config as csv_config
from apps.base.models.facts.services.backstage.fact_services_backstage_asset_match import FactServicesBackstageAssetMatch
from apps.base.models.dimensions.dimension_client import DimensionClient
from apps.base.models.utilities.client import Clients
from apps.cubes.models.daily.license_delivery_raw import CubeLicenseDeliveryRawDaily
from apps.cubes.models.daily.store_transaction import CubeStoreTransaction
from apps.cubes.models.daily.asset_match import CubeAssetMatch
from apps.cubes.models.daily.registration_raw import CubeRegistrationRawDaily

from django.db.models.query import ValuesQuerySet

import logging
log = logging.getLogger('reporting')


class CSVgenerator():

    REPORT_DATA = {
        'registrations-raw': CubeRegistrationRawDaily.raw,
        'subscriptions': CubeSubscriptionsDaily.test,
        'content':  CubeAssetMatch.get_data,
        'subscription_revenue': CubeSubscriptionRevenueDaily.raw,
        'license': CubeLicenseDeliveryRawDaily.raw,
        'transaction': CubeStoreTransaction.get_data
    }


    CUBE_NAMES = {
        'registrations-raw': CubeRegistrationsDaily,
        'subscriptions': CubeSubscriptionsDaily,
        'content': CubeAssetMatch,
        'subscription_revenue': CubeSubscriptionRevenueDaily,
        'license': CubeLicenseDeliveryRawDaily,
        'transaction': CubeStoreTransaction
    }
    REPORT_CONFIG = {
        'content': 'CONTENT_SETTINGS'
    }

    def __init__(self, report_type=None, client_id='all', args=None):

        self._client_id = client_id
        self._report_type = report_type
        self._client_name = ''
        self._attributes = []
        if not args:
            try:
                sftp_settings = getattr(settings, 'SFTP_SETTINGS', None)
                if not sftp_settings:
                    raise Exception('SFTP settings not found.')

                self._sftp_settings = sftp_settings[self._report_type] \
                    if self._report_type in sftp_settings else sftp_settings['DEFAULT']

                report_settings = getattr(settings, 'SERVICE_SETTINGS', None)

                if not report_settings:
                    raise Exception('SERVICE SETTINGS settings not found.')

                self._report_settings = report_settings[self._report_type] \
                    if self._report_type in report_settings else report_settings['DEFAULT']
            except Exception:
                log.exception('')

            if not self._report_settings or not self._sftp_settings:
                log.debug('CSV config not found in settings.')
                raise Exception('CSV config not found in settings.')
            else:

                self._config = csv_config.get(self._report_type)

                if not self._config:
                    log.debug('No CSV config found for {}'.format(report_type))

            start_date, end_date = self.get_dates(
                self._report_settings.get('report_frequency', 'weekly')
            )
            self._report_params = (self._client_id, start_date, end_date)

        else:
            self._config = csv_config.get(args[0], None)  # request path
            client_id = self._config.split('/')[0]
            self._report_params = (client_id, args[1], args[2])  # start and end dates
        self._values = list()

    def get_dates(self, freq):
        today = datetime(
            day=datetime.utcnow().day,
            month=datetime.utcnow().month,
            year=datetime.utcnow().year
        )
        if freq == 'weekly':
            e = today - timedelta(days=1)
            s = e - timedelta(days=6)
            return s.date(), e.date()

    def get_registration_path_attributes(self, path):
        attr = self._config.get('request_paths_format')
        rep = path.split('/')
        filters = rep[4:6]
        filters = {i[0]: i[1] for i in zip(['territory_code', 'platform_name'], filters)}
        attr = {i[0]: i[1] for i in zip(attr, rep)}

        if attr['client_id'] != 'all':
            filters['client_id'] = attr['client_id']

        return attr, filters

    def get_content_report_attributes(self, path):

        attr = self._config.get('request_paths_format')
        attr = {i[0]: i[1] for i in zip(attr, path.split('/'))}

        filters = {
            k: v for k, v in attr.iteritems()
            if k in ['client_id', 'start_date', 'end_date'] and v != 'all'
        }

        return attr, filters

    def get_license_attributes_and_filters(self, path):
        filters = dict()
        attr = dict()
        params = path.split('/')
        client_id = params[0]
        if client_id != 'all':
            filters['client_id'] = client_id

        attr['client_id'] = client_id
        attr['start_date'] = params[len(params)-2]
        attr['end_date'] = params[len(params)-1]
        return attr, filters

    def get_transaction_attributes_and_filters(self, path):
        filters = dict()
        attr = dict()
        params = path.split('/')
        client_id = params[0]
        if client_id != 'all':
            filters['client_id'] = client_id

        attr['client_id'] = client_id
        attr['start_date'] = params[len(params)-2]
        attr['end_date'] = params[len(params)-1]
        return attr, filters

    def get_subscription_revenue_attributes_and_filters(self, path):
        filters = dict()
        attr = dict()
        params = path.split('/')
        client_id = params[0]

        if client_id != 'all':
            filters['client_id'] = client_id

        attr['client_id'] = client_id
        attr['start_date'] = params[len(params)-2]
        attr['end_date'] = params[len(params)-1]

        return attr, filters

    def generate(self):

        GET_ATTRIBUTES = {
            'registrations-raw': self.get_registration_path_attributes,
            'content': self.get_content_report_attributes,
            'license': self.get_license_attributes_and_filters,
            'transaction': self.get_transaction_attributes_and_filters,
            'subscription_revenue': self.get_subscription_revenue_attributes_and_filters
        }

        today = datetime(
            day=datetime.utcnow().day,
            month=datetime.utcnow().month,
            year=datetime.utcnow().year
        )

        data = list()
        cube = ''

        csvdata = dict()
        request_path_number = 0

        for i in self._config['request_paths']:
            try:
                path = i.format(*self._report_params)

                self._values = list()
                report_name = path.split('/')[1]
                attributes, filters = GET_ATTRIBUTES[report_name](path)

                self._attributes = attributes

                st_date = attributes.get('start_date', today - timedelta(days=7))
                end_date = attributes.get('end_date', today)

                start = datetime.strptime(st_date, settings.DATE_FORMAT_YMD) if isinstance(st_date, str) else st_date
                end = datetime.strptime(end_date, settings.DATE_FORMAT_YMD) if isinstance(end_date, str) else end_date

                start, end, date_range = get_date_range(
                    start,
                    end,
                    cube=self.CUBE_NAMES[report_name],
                    interval=attributes.get('interval', 'weekly')
                )
            except Exception:
                log.exception('\n---\n')
                raise Exception('Error occurred while processing request attributes.')

            try:
                if not date_range:
                    date_range = [(start, end)]

                for s, e in date_range:

                    data = CSVgenerator.REPORT_DATA[report_name](
                        s,
                        e,
                        filters,
                        attributes.get('group', 'all'),
                    )

                    if data:
                        if not isinstance(data, list) and \
                                not isinstance(data, ValuesQuerySet):

                            self.format_data(data, s, e, attributes)
                        elif isinstance(data, list) or isinstance(data, ValuesQuerySet):
                            for rec in data:
                                self.format_data(rec, s, e, attributes)

                csvdata[request_path_number] = self._values
                request_path_number += 1
            except Exception as e:
                log.exception('Exception occurred while creating data for csv report.')
                raise Exception('Exception occurred while creating data for csv report. {}'.format(e.args))


        try:

            rep_file_name = self._report_settings.get('report_filename', '{}_'+self._report_type+'_{}')

            file_name = rep_file_name.format(
                self.get_client_name_for_file(),
                start.strftime(settings.DATE_FORMAT_YMD)
            )

            file_path = join(settings.REPORTS_ROOT, file_name)
            report_file = open(file_path, 'wb')
            #take headers from config file instead of values.
            config_headers = self._config['headers']
            csv_headers = [str(h['csvfield'])for h in config_headers]


            myWriter = csv.DictWriter(
                report_file,
                fieldnames=csv_headers,
                dialect='excel'
            )
            headers = dict(
                (n, str(n).title()) for n in csv_headers
            )
            myWriter.writerow(headers)

            if len(csvdata[0]):

                for row in range(0, len(csvdata[0])):

                    try:
                        row_list = list()
                        for h in config_headers:
                            t = (
                                h['csvfield'],
                                csvdata[h['repnbr']][row][h['dbfield']] if h['dbfield'] else ''
                            )
                            row_list.append(t)

                        csv_row = dict(row_list)

                    except Exception as e:
                        log.exception('Exception while writing row to CSV file.')
                        raise Exception('EXCEPTION WHILE CREATING CSV ROW FROM GIVEN CONFIG.')
                    myWriter.writerow(csv_row) if csv_row else ''

            report_file.close()

        except Exception:
            log.exception('')
            raise Exception('Exception occurred while creating csv report file.')
        try:
            self.upload_report(file_path, file_name, start)
        except Exception:
            log.exception('')
            raise Exception('Exception while uploading report.')

        return cube

    def format_data(self, data, s, e, attributes):
        name = {'daily': s.strftime("%A"),
                'weekly': s.strftime("%W"),
                'monthly': s.strftime("%b"),
                'total': 'Total'}

        if attributes.get('group', 'all') == 'all':
            x = {'start': s.strftime(settings.DATE_FORMAT_YMD),
                     'end': e.strftime(settings.DATE_FORMAT_YMD),
                     'name': name[attributes.get('interval', 'total')]}
            if not data:
                data = dict()

            data.update({'start': s.strftime(settings.DATE_FORMAT_YMD),
                         'end': e.strftime(settings.DATE_FORMAT_YMD),
                         'name': name[attributes.get('interval', 'total')]})
            self._values.append(data)
        else:
            if data:
                for k, v in data.iteritems():
                    if isinstance(v, dict):
                        v.update({'start': s.strftime(settings.DATE_FORMAT_YMD),
                                     'end': e.strftime(settings.DATE_FORMAT_YMD),
                                     'name': name[attributes.get('interval', 'total')]})
                        v['group'] = k
                        self._values.append(v)

    def get_cube_name(self, request_path):
        if isinstance(request_path, str):
            if len(request_path.split('/')):
                return request_path.split('/')[1]

    def upload_report(self, filepath, file_name, report_date):
        """
        >>> a = CSVgenerator('123')
        >>> a.upload_report(None, 'upload.txt', '2014-05-06')
        """
        # appropriate changes required for doc test to run - dev only.
        # test_file_path = join(settings.REPORTS_ROOT, '16b6a354-ff32-4be4-b648-fe51fc5b1508.csv')
        # # trace.info('----- {}'.format(abspath(test_file_path)))
        # absolute_filename = abspath(test_file_path)
        # test_filename = '16b6a354-ff32-4be4-b648-fe51fc5b1508.csv'

        #TODO remove after QA testing.
        if not filepath:
            test_file_path = join(settings.REPORTS_ROOT, file_name)
            absolute_filename = abspath(test_file_path)
        else:
            absolute_filename = abspath(filepath)

        try:
            report_date = report_date if isinstance(report_date, str) else report_date.strftime(settings.DATE_FORMAT_YMD)
        except Exception:
            log.exception('')

        try:
            #TODO use sftp credentials, once available.
            #TODO get client upload location for per-client report.
            # ftp_client_dir = client.ftp_client_dir
            # if ftp_client_dir == '':
            #     ftp_client_dir = getattr(settings, 'DEFAULT_SFTP_LOCATION', 'default')
            #     logger.exception(u'No FTP configuration for client {} using default value.'.format(client.name))
            #

            year_folder, month_folder, _ = report_date.split('-')

            base_folder_path = self._sftp_settings.get('path', '')

            base_path = base_folder_path.split('/')
            base_folders = [i for i in base_path[1:-1]]
            base_folder = '/' + join(*base_folders)
            env_folder = str(base_path[-1:][0])

            from paramiko import Transport, SFTPClient
            try:
                log.info(u'SFTP logging on to {0} as {1}'.format(settings.SFTP_SERVER, settings.SFTP_USERNAME))
                transport = Transport((
                    self._sftp_settings.get('server', ''),
                    self._sftp_settings.get('port', 22))
                )
                transport.connect(
                    username=self._sftp_settings.get('username', ''),
                    password=self._sftp_settings.get('password', '')
                )
                sftp = SFTPClient.from_transport(transport)
                log.info(u'SFTP dir {0}/{1}/{2}/{3}'.format(base_folder, env_folder, year_folder, month_folder))
                try:
                    sftp.chdir(base_folder)
                except Exception:
                    log.debug('Unable to change to base folder on ftp server.')

                self._make_or_change_sftp_dir(sftp, env_folder)
                self._make_or_change_sftp_dir(sftp, year_folder)
                self._make_or_change_sftp_dir(sftp, month_folder)

                log.debug(u'SFTP uploading {0}'.format(filepath))
                sftp.put(absolute_filename, file_name)
            except Exception:
                log.exception(u'Unrecoverable exception during SFTP upload process.')

            finally:
                log.debug(u'SFTP logging off')

                try:
                    sftp.close()
                except Exception:
                    log.exception(u'SFTP exception while closing SFTP session.')

                try:
                    transport.close()
                except Exception:
                    log.exception(u'SFTP exception while closing SSH connection.')

        except Exception:
            log.debug('Error while uploading report.')

    def _make_or_change_sftp_dir(self, sftp, dirname):
        """
        Try to change to the given directory on the given SFTP connection.
        If that fails, make the directory and try changing directory again.
        """
        try:
            sftp.chdir(dirname)
        except IOError:
            sftp.mkdir(dirname)
            sftp.chdir(dirname)

    def get_client_location(self):
        #TODO update once server credentials available.
        return 'dev'

    def get_ripe_client_id(self, ext_client_id):
        res = '123'
        try:
            res = int(DimensionClient.objects.get(client_id=ext_client_id).id)
        except Exception:
            log.info('Ripe client-ID not found for {}'.format(ext_client_id))
        return res

    def get_client_name_for_file(self):
        client_name = self._attributes.get('client_id', '')
        if client_name == 'all':
            return 'AllClients'
        try:
            client_name = str(Clients.objects.get(id=self._attributes['client_id']).name)
        except Exception as e:
            log.info('client_id: {}. Exception: {}'.format(self._attributes['client_id'], e.message))
        return client_name if client_name else self._client_id

