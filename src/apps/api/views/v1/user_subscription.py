from django.views.decorators.http import require_http_methods
from nexus.decorators import server_to_server_auth
from saffron.api.response.base import ApiSuccessHttpResponse
from apps.api.exception import RipeApiException
from apps.api.helpers import dates
#from apps.api.helpers.auth import get_secret_by_access_key
from apps.reporting.utils.build_csv import BuildCsv
from apps.cubes.models.daily.subscriptions import CubeSubscriptionsDaily
from apps.api.helpers.response import ResponseGenerator
from apps.api.helpers.mapper import Mapper
from collections import Counter
from apps.api.helpers import dates
from django.forms.models import model_to_dict

import logging
logger = logging.getLogger('reporting')
trace = logging.getLogger('subscriptions')
import datetime

DT_FORMAT = "%Y-%m-%d"
SUBS_STRUCT = {'new': 0, 'total': 0, 'average': 0, 'start': '', 'end': '', 'name': ''}
GROUP_SUBS_SRUCT = {'group': {'new': 0, 'total': 0, 'average': 0}, 'start': '', 'end': '', 'name': ''}
SUBS_ATTRIBUTES = ['client', 'api', 'group', 'interval', 'territory', 'platform', 'start_date', 'end_date']




@require_http_methods(['GET'])
#@server_to_server_auth(get_secret_by_access_key)
def total_subscription_report(
        request,
        client,
        package,
        state,
        group,
        territory,
        platform,
        start_date,
        end_date, **kwargs):

    try:
        start_date = str(start_date) if start_date else 'all'
        # use this for asserting whether we respond in json, or use CSV only allow either...
        response_format = str(request.GET.get('format', 'json')).lower()
        if start_date != 'all':
            dates.character_checker(start_date)
            dates.character_checker(end_date)
            start = datetime.datetime.strptime(start_date, DT_FORMAT).date()
            end = datetime.datetime.strptime(end_date, DT_FORMAT).date()
            if end < start:
                raise RipeApiException(
                    *RipeApiException.BAD_DATE_RANGE,
                    debug_message=u"End date '{}' is before '{}'".format(end, start)
                )
        else:
            start = datetime.datetime.strptime('01-01-1977', DT_FORMAT).date()
            end = datetime.datetime.strptime('01-01-2999', DT_FORMAT).date()


        group_key = group
        group = str(group) if group else 'all'


        params = {'client': client or 'all',
                  'platform': platform or 'all',
                  'territory': territory or 'all',
                  'package': package or 'all',
                  'user_state': state or 'active'}

        filters = {}


        for k in params:
            if params[k] != 'all':
                filters[k] = str(params[k])



        # package is an exception
        filters['package'] = package

        fc = CubeSubscriptionsDaily.objects.filter(
            client_id=client,
            #package=
            subscription_state=state,
            #group=
            territory_code=territory,
            #platform=
            date__gte=start,
            date__lte=end
        ).latest('date')

        #if kwargs.get('interval', None) == 'monthly':
        #    try:
        #        results = SUBSCRIPTIONS.subscriptions.monthly(filters, group, start_date, end_date)
        #    except Exception:
        #        trace.exception('\n\n')
        #elif kwargs.get('interval', None) == 'weekly':
        #    try:
        #        results = SUBSCRIPTIONS.subscriptions.weekly(filters, group, start_date, end_date)
        #    except Exception:
        #        trace.exception('\nWEEKLY VIEW\n')
        #elif kwargs.get('interval', None) == 'daily':
        #    try:
        #        results = SUBSCRIPTIONS.subscriptions.daily_summary(filters, group, start_date, end_date)
        #    except Exception:
        #        trace.exception('\n---daily view---\n')
        #
        #else:
        #    try:
        #        results = SUBSCRIPTIONS.subscriptions.total(filters, group, start_date, end_date)
        #    except Exception:
        #        trace.exception('\n TOTAL IN RIPE API \n\n')
        #
        #previous_report = False
        #if start_date != 'all':
        #    previous_start_date, previous_end_date = dates.previous_report_date(start_date, end_date)
        #
        #    previous_results = SUBSCRIPTIONS.subscriptions.total(
        #        filters, group, previous_start_date, previous_end_date)
        #
        #    previous_report = True
        results = model_to_dict(fc)

        if response_format == 'json':
            results['attributes'] = {
                "client":       client,
                "package":      package,
                "state":        state,
                "groupby":      group_key,
                "territory":    territory,
                "platform":     platform,
                "start_date":   start_date,
                "end_date":     end_date,
                }

            # trace.info('DAILY SUMMARY RESULTS IN VIEW - 1 : {}\n'.format(results))
            # TODO
            #if previous_report and start != end:
            #    previous_results['attributes'] = {
            #        "client":       client,
            #        "package":      package,
            #        "state":        state,
            #        "groupby":      group_key,
            #        "territory":    territory,
            #        "platform":     platform,
            #        "start_date":  previous_start_date,
            #        "end_date":    previous_end_date
            #    }

            # trace.info('DAILY SUMMARY RESULTS IN VIEW - 2 : {}\n'.format(results))

            result = {
                "user_subscription": {
                    "current_report": results,
                    }
            }

            # TODO
            #if previous_report:
            #    result['user_subscription']['previous_report'] = previous_results


            # trace.info(' CURR REP : \n{}\n'.format(result['user_subscription']['current_report'].keys()))
            # trace.info(' FINAL REP : \n{}\n'.format(result['user_subscription']['current_report']))

            return ApiSuccessHttpResponse(result)
        elif response_format == 'csv':
            csv = BuildCsv()
            csv.input_json_structure(
                json=results
            )
            csv.build()
            return csv.response("subscriptions")
        else:
            raise RipeApiException(
                *RipeApiException.API_FORMAT,
                debug_message=u"format selection '{}' is not a valid format type".format(response_format)
            )
    except Exception:
        trace.exception('\n--??--\n')