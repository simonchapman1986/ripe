from apps.flags.models.flag import Flags

import logging

logger = logging.getLogger('reporting')

# a set of constants for flag registration types
DOES_NOT_EXIST = 'DoesNotExist'
UNEXPECTED_RESULT = 'UnexpectedResult'
MISSING_DATA = 'MissingData'
BAD_DATA = 'BadData'
UNEXPECTED_EVENT = 'UnexpectedEvent'
BUSINESS_RULE_NOT_MET = 'BusinessRuleNotMet'
MISSING_EVENT_OCCURRENCE = 'MissingEventOccurrence'


def register_flag(type='default', description='default', event='default'):
    """
    register_flag

    An issue has been risen, we need to register this flag we take our generic data and pass to the create_flag
    class method of Flags, we also put in a log warning about this.
    """

    Flags.create_flag(
        **{
            "name":         type,
            "description":  description,
            "event":        event
        }
    )
    logger.warning('FLAG:\n{}\n{}\n{}'.format(
        type,
        description,
        event
    ))