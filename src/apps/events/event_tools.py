import json
import logging
import functools


logger = logging.getLogger('reporting')


def parse_args_as_json(event_name):
    def decorator(fn):
        @functools.wraps(fn)
        def decorated(string):
            data = json.loads(string)
            logger.debug("Received event %s: '%s'", event_name, data)
            fn(data)
            logger.debug("Handled event %s: '%s'", event_name, data)
        return decorated
    return decorator
