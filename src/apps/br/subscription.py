from apps.base.models.dimensions.dimension_subscription_status import subscription_status_lookup

from apps.flags.report import register_flag
from apps.flags.report import BUSINESS_RULE_NOT_MET

# status
INACTIVE = 'inactive'
ACTIVE = 'active'
EXPIRED = 'expired'
CANCELLED = 'cancelled'
LAPSED = 'lapsed'
PAYMENT_PENDING = 'payment_pending'

# window types
ONGOING = 'ongoing'
FIXED = 'fixed'


RNS = 'registered_never_subscribed'
SF = 'subscriber_fixed'
SO = 'subscriber_ongoing'
WSL = 'was_subscribed_lapsing'
WSC = 'was_subscribed_cancelling'
WSLI = 'was_subscribed_lapsed_inactive'
WSCI = 'was_subscribed_cancelled_inactive'
WSE = 'was_subscribed_expired'

# current_state, next_state, event
user_sub_ongoing = [
    (RNS,   SO,     ACTIVE),
    (WSLI,  SO,     ACTIVE),
    (WSCI,  SO,     ACTIVE),
    (WSE,   SO,     ACTIVE),
    (WSL,   SO,     ACTIVE),
    (WSC,   SO,     ACTIVE),
    (SF,    WSE,    EXPIRED),
    (SO,    WSE,    EXPIRED),
    (SF,    WSL,    LAPSED),
    (SO,    WSL,    LAPSED),
    (SF,    WSC,    CANCELLED),
    (SO,    WSC,    CANCELLED),
    (WSL,   WSC,    CANCELLED),
    (WSL,   WSLI,   INACTIVE),
    (RNS,   RNS,    INACTIVE),
    (WSC,   WSCI,   INACTIVE),
]

user_sub_not_ongoing = [
    (RNS,   SF,     ACTIVE),
    (WSLI,  SF,     ACTIVE),
    (WSCI,  SF,     ACTIVE),
    (WSE,   SF,     ACTIVE),
    (WSL,   SF,     ACTIVE),
    (WSC,   SF,     ACTIVE),
    (SF,    WSE,    EXPIRED),
    (SO,    WSE,    EXPIRED),
    (SF,    WSL,    LAPSED),
    (SO,    WSL,    LAPSED),
    (SF,    WSC,    CANCELLED),
    (SO,    WSC,    CANCELLED),
    (WSL,   WSC,    CANCELLED),
    (WSL,   WSLI,   INACTIVE),
    (RNS,   RNS,    INACTIVE),
    (WSC,   WSCI,   INACTIVE),
]


def get_rule(status=0, current_state=RNS, window_ongoing=False):
    """
    >>> get_rule(status=0, current_state=RNS, window_ongoing=True)
    'registered_never_subscribed'
    >>> get_rule(status=1, current_state=RNS, window_ongoing=True)
    'subscriber_ongoing'
    >>> get_rule(status=1, current_state=RNS, window_ongoing=False)
    'subscriber_fixed'
    """
    # default to current state
    next_state = current_state
    _ov = False
    err = False

    # get string of our status
    _status = subscription_status_lookup[int(status)]

    ## if we are an active lets generate, else...
    #sub_status = "{}-{}".format(
    #    subscription_status_lookup[status],
    #    ONGOING if window_ongoing else FIXED) if _status == ACTIVE else _status
    if window_ongoing:
        user_sub = user_sub_ongoing
    else:
        user_sub = user_sub_not_ongoing


    # look through the possibilities and break out if we match
    for current, next_state, event in user_sub:
        if event == _status:
            if current == current_state:
                _ov = True
                break

    if not _ov:
        # error state.. we will use current to continue
        # lets flag the error
        register_flag(
            type=BUSINESS_RULE_NOT_MET,
            description='recieved status({}) with current_state({}) - failed to match business rule'.format(
                _status,
                current_state
            ),
            event='subscription'
        )
        # flag an error state
        err = True


    return next_state, err


def ignore_event(event, state, ongoing):
    """
    To assert whether we continue to total up.. or use previous 'like' aggregated totals
    """
    if ongoing:
        state_diagram = user_sub_ongoing
    else:
        state_diagram = user_sub_not_ongoing

    for _, _state, _event in state_diagram:
        if _state==state and _event==event:
            return False

    return True
