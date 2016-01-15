from saffron.api.exception import ApiExceptions, ApiException


class RipeApiException(ApiException):
    """
    NAME_OF_EXCEPTION = ApiExceptions.register(
        u'string of message',
        1001  # error no
        ApiException.HTTP_SERVER_ERROR  # error type
    )
    """
    # Api exceptions
    CHARACTER_CHECK_FAILURE = ApiExceptions.register(
        u'Illegal characters detected',
        1001,
        ApiException.HTTP_SERVER_ERROR
    )

    # Subscriptions API
    SUBSCRIPTION_TOTALS = ApiExceptions.register(
        u'Unable to retrieve Subscription Totals',
        2001,
        ApiException.HTTP_SERVER_ERROR
    )

    # Subscriptions API
    API_FORMAT = ApiExceptions.register(
        u'Invalid API format',
        2002,
        ApiException.HTTP_SERVER_ERROR
    )

    # Helper exceptions
    INCORRECT_PERIOD_PREVIOUS_REPORT = ApiExceptions.register(
        u'An invalid period type was set for previous report date',
        3001,
        ApiException.HTTP_SERVER_ERROR
    )

    # model exceptions
    MODEL_BAD_SUBSCRIPTION_STATE = ApiExceptions.register(
        u'Invalid subscription State',
        9001,
        ApiException.HTTP_BAD_REQUEST
    )

    MODEL_BAD_DATE_FORMAT = ApiExceptions.register(
        u'Invalid date format',
        9002,
        ApiException.HTTP_BAD_REQUEST
    )

    MODEL_BAD_SUBSCRIPTION_PACKAGE = ApiExceptions.register(
        u'Invalid subscription Package',
        9003,
        ApiException.HTTP_BAD_REQUEST
    )

    BAD_DATE_RANGE = ApiExceptions.register(
        u'End date is before start date.',
        2003,
        ApiException.HTTP_SERVER_ERROR
    )

    BAD_CUBE = ApiExceptions.register(
        u'Unable to calculate date range.',
        9004,
        ApiException.HTTP_SERVER_ERROR
    )
