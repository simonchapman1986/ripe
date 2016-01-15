from django.views.decorators.http import require_http_methods
from apps.api.helpers.dates import get_date_range
from django.db.models import Sum
from nexus.decorators import server_to_server_auth
from saffron.api.response.base import ApiSuccessHttpResponse
from apps.api.exception import RipeApiException
from apps.api.helpers import dates
#from apps.api.helpers.auth import get_secret_by_access_key
from apps.reporting.utils.build_csv import BuildCsv
from apps.cubes.models.daily.registrations import CubeRegistrationsDaily as registration
from apps.api.helpers.response import ResponseGenerator
from apps.api.helpers.mapper import Mapper
from collections import Counter


import logging
logger = logging.getLogger('reporting')
trace = logging.getLogger('trace')
import datetime

DT_FORMAT = "%Y-%m-%d"
REG_STRUCT = {'new': 0, 'total': 0, 'average': 0, 'start': '', 'end': '', 'name': ''}
GROUP_SUMMARY_STRUCT = {'new': 0, 'total': 0, 'average': 0}
GROUP_REG_SRUCT = {'start': '', 'end': '', 'name': ''}
REG_ATTRIBUTES = ['client', 'api', 'group', 'interval', 'territory', 'platform', 'start_date', 'end_date']



@require_http_methods(['GET'])
# @server_to_server_auth(get_secret_by_access_key)
def registration_report(
        request,
        client,
        group,
        territory,
        platform,
        start_date,
        end_date, **kwargs):

    # use this for asserting whether we respond in json, or use CSV only allow either...
    response_format = str(request.GET.get('format', 'json')).lower()
    try:
        start_date = str(start_date) if start_date else 'all'
        end_date = str(end_date) if end_date else 'all'
    except Exception as e:
        return ApiSuccessHttpResponse(body={'status': '{}'.format(e.message)}, http_code=500)
    try:
        #if start_date != 'all':
        #    dates.character_checker(start_date)
        #if end_date != 'all':
        #    dates.character_checker(end_date)
        #dt = [start_date, end_date]
        #dt_dates = [datetime.datetime.strptime(d, DT_FORMAT).date() if d != 'all' else d for d in dt]
        # trace.info('dates: {}'.format(dt_dates))
        try:
            if start_date != 'all':
                start = datetime.datetime.strptime(start_date, DT_FORMAT).date()
            else:
                start = 'all'
            if end_date != 'all':
                end = datetime.datetime.strptime(end_date, DT_FORMAT).date()
            else:
                end = 'all'
        # trace.info('s: {} e: {}'.format(start, end))
        #if isinstance(start, datetime.date) and isinstance(end, datetime.date):
        #    if end < start:
        #        raise RipeApiException(
        #            *RipeApiException.BAD_DATE_RANGE,
        #            debug_message=u"End date '{}' is before '{}'".format(end, start)
        #        )
        except Exception as e:
            return ApiSuccessHttpResponse(body={'status': '{}'.format(e.message)}, http_code=200)

        group_key = group
        group = str(group) if group else 'all'

        params = {'client': client or 'all',
                  'platform': platform or 'all',
                  'territory': territory or 'all'}
        filters = {}
        # print 'ALL reg PARAMS: {}'.format(params)
        for k in params:
            if params[k] != 'all':
                filters[k] = str(params[k])

        trace.info('FILTERS: {}'.format(filters))
        trace.info('GROUP: {}'.format(group))

        #creates the structure.
        try:
            # trace.info('getting DATE RANGE BETWEEN: \ns:{} e: {}\n'.format(start, end))
            start, end, date_range = get_date_range(
                start,
                end,
                cube=registration,
                interval=kwargs.get('interval', None)
            )
            # trace.info('----------s:{} e: {}, range: {} range LEN: {}'.format(start, end, date_range, len(date_range)))

            if group == 'all':
                gen = ResponseGenerator('registrations',
                                        request.path,
                                        REG_ATTRIBUTES,
                                        REG_STRUCT,
                                        len(date_range) if len(date_range) else 1)
            else:
                trace.info('-----GROUPS BY {}------'.format(group))
                struct_with_groups = dict()
                struct_with_groups.update({'start': '', 'end': '', 'name': ''})
                grp_struct = {}
                # trace.info('----before struct {}'.format(grp_struct))

                #finds number of groups.
                groups, group_name = registration.get_groups(group)

                #FILTERED-GROUPS
                if group in filters:
                    # trace.info('----filtering groups: {} by {}'.format(group, filters[group]))
                    grp_struct.update({filters[group]: GROUP_SUMMARY_STRUCT})
                    # trace.info('----after struct FILTERED GRP {}'.format(grp_struct))
                else:
                    # trace.info('----all groups: {}'.format())
                    if groups:
                        trace.info('--creating struct for ALL groups: ---, group-name: {}, groups: {}'.format(group_name, groups))
                        for i in groups:
                            grp_struct.update({i[group_name]: GROUP_SUMMARY_STRUCT})
                        # trace.info('----after struct ALL GRP {}'.format(grp_struct))
                    else:
                        trace.info('{}')



                # trace.info('---- grp struct {}'.format(grp_struct))
                struct_with_groups.update(grp_struct)
                # trace.info('----curr rep struct {}'.format(struct_with_groups))
                gen = ResponseGenerator('registrations',
                                        request.path,
                                        REG_ATTRIBUTES,
                                        struct_with_groups,
                                        len(date_range) if len(date_range) else 1)
            gen.set_report_template()
            struct = gen.get_dict_response()
            trace.info('STRUCT created: '.format(struct))
        except Exception as e:
            return ApiSuccessHttpResponse(body={'status': '{}'.format(e.message)}, http_code=200)

        try:
            m = Mapper(struct)
            if not date_range:
                date_range = [(start, end)]
            i = 0
            for s, e in date_range:
                #if group == 'all':
                #    data = registration.get_total(filters, s, e, group)
                #    name = {'daily': s.strftime("%A"),
                #            'weekly': s.strftime("%W"),
                #            'monthly': s.strftime("%b"),
                #            'total': 'total'}
                #    data.update({'start': s.strftime(DT_FORMAT),
                #                 'end': e.strftime(DT_FORMAT),
                #                 'name': name[kwargs.get('interval', '')]})
                #    m.map_to_struct(Counter(data), 'current_report', i)
                #else:

                    #GROUPS
                ds = dict()
                ds.update({'start': s.strftime(DT_FORMAT),
                           'end': e.strftime(DT_FORMAT),
                           'name': 'test'})

                data = registration.get_total(filters, s, e, group)

                ds.update(data[0])
                #return ApiSuccessHttpResponse(body={'status': '{}'.format(ds)}, http_code=200)

                # trace.info('UPDATING LOC {} OF STRUCT {}'.format(i, struct))
                #from collections import Counter
                ##return ApiSuccessHttpResponse(body={'status': '{}'.format(Counter(ds))}, http_code=200)
                #ds = Counter(ds)
                #m.map_to_struct(ds, 'current_report', i)
                #i += 1
                struct = {'current_report': ds}

            # trace.info(' POPULATED STRUCT : {}'.format(struct))
        except Exception as e:
            return ApiSuccessHttpResponse(body={'status': '{}'.format(e)}, http_code=200)

        # previous_report = False
        # if start_date != 'all':
        #     previous_start_date, previous_end_date = dates.previous_report_date(start_date, end_date)
        #
        #     previous_results = CubeRegistrationsDaily.cube.total(
        #         filters, group, previous_start_date, previous_end_date)
        #
        #     previous_report = True

        result = struct

        if response_format == 'json':

            # results['attributes'] = {
            #     "client":       client,
            #     "groupby":      group_key,
            #     "territory":    territory,
            #     "platform":     platform,
            #     "start_date":   start_date,
            #     "end_date":     end_date,
            #     }

            # if previous_report and start != end:
            #     previous_results['attributes'] = {
            #         "client":       client,
            #         "groupby":      group_key,
            #         "territory":    territory,
            #         "platform":     platform,
            #         "start_date":  previous_start_date,
            #         "end_date":    previous_end_date
            #     }

            pass
            # if previous_report:
            #     result['user_subscription']['previous_report'] = previous_results
        elif response_format == 'csv':
            csv = BuildCsv('registrations')
            csv.input_json_structure(
                json=result
            )
            csv.build()
            return csv.response("registrations")
        else:
            raise RipeApiException(
                *RipeApiException.API_FORMAT,
                debug_message=u"format selection '{}' is not a valid format type".format(response_format)
            )

        return ApiSuccessHttpResponse(result)
    except Exception:
        trace.exception('\n---\n')


