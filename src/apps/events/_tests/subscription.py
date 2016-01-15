import json
import datetime
from uuid import uuid4

from django.utils.timezone import now
from django.test import TestCase

from hamcrest import assert_that
from hamcrest import has_length
from hamcrest import has_properties
from hamcrest import contains_inanyorder

from apps.base.models import FactServicesStorefrontSubscription
from apps.base.models.dimensions.dimension_client import DimensionClient
from apps.base.models.dimensions.dimension_platform import DimensionPlatform
from apps.base.models.dimensions.dimension_subscription_state import DimensionSubscriptionState
from apps.base.models.dimensions.dimension_subscription_status import DimensionSubscriptionStatus
from apps.base.models.dimensions.dimension_subscription_type import DimensionSubscriptionType
from apps.base.models.dimensions.dimension_territory import DimensionTerritory
from apps.base.models.dimensions.dimension_user import DimensionUser
from apps.base.models.dimensions.dimension_utc_date import DimensionUTCDate

from apps.flags.report import DOES_NOT_EXIST
from apps.flags.checks.client import DESCRIPTION
from apps.flags.models.flag import Flags

from apps.events.storefront.subscription import user_subscription


when = now().replace(microsecond=0)


class TestStorefrontEvents(TestCase):
    """
    TestStorefrontEvents

    Testcase to test the end-to-end flow of an incoming subscription event
    RabbitMQ ingestion --> fact table storage


    Here we create some dummy data sets, as a JSON stuc and parse it to the event task as if ingested.
    We then assert whether with the given data, we get the correct I/O we desire.

    We assert things such as;
        * the dimensions it created.
        * the data that resides in the newly created fact
        * the error flags raised

    We use our dim_utc_date fixture to populate our utc_date table so our foreign keys work.

    Flags:

    The reason we have flags raised is because the data we use is based on the rules set out by the dimensions.
    These are dim-by-dim specific rules that act globally in the RIPE service.

    Certain dims rely on previous acts having occurred, we never ignore the data coming in, but there may be occasions
    whereby we receive events prior to an event happening in a different case; i.e. ingesting clients.
    When this does occur, we flag it. This is so we register the alert to look into why/or how this could have
    happened. Its not an end-of-the-world state, but could do with attention.
    """

    fixtures = ['dim_utc_date.json']


    def test_initial_injestion(self):
        # clear out
        FactServicesStorefrontSubscription.objects.all().delete()
        Flags.objects.all().delete()

        # sample uuids
        i_uid = str(uuid4())
        e_uid = str(uuid4())
        c_id = str(uuid4())
        sub_id = str(uuid4())
        win_id = str(uuid4())
        item_id = str(uuid4())
        prod_id = str(uuid4())
        win_price_id = str(uuid4())
        win_usage_right_id = str(uuid4())
        apple_prod_id = str(uuid4())
        tran_id = str(uuid4())

        win_start = datetime.datetime(year=2013, month=1, day=1).strftime("%Y-%m-%d")
        win_end = datetime.datetime(year=2030, month=1, day=1).strftime("%Y-%m-%d")

        # dict structure for out mock event
        data = {
            'window_id':                win_id,
            'item_id':                  item_id,
            'product_id':               prod_id,
            'window_start_date':        win_start,
            'window_end_date':          win_end,
            'window_pricing_id':        win_price_id,
            'window_usage_right_id':    win_usage_right_id,
            'window_tier':              'TEST',
            'window_deleted_date':      '',                     # we wont necessarily have this more likely not
            'window_type':              'master',
            'window_on_going':          1,
            'window_repeat_count':      1,
            'window_auto_upgrade':      1,
            'window_allow_repurchase':  1,
            'apple_product_id':         apple_prod_id,
            'transaction_id':           tran_id,
            'internal_user_id':         i_uid,
            'external_user_id':         e_uid,
            'territory':                'GB',
            'client_id':                c_id,
            'subscription_id':          sub_id,
            'subscription_period':      'P1M',
            'subscription_recurrence':  '1',
            'subscription_status':      0,                      # inactive
            'platform_os':              'iOS',
            'platform_name':            'test-ios-platform',
            'platform_version':         '7.1.0',
            'event_time':               str(when),
            }

        # json encode our data string to replicate ingestion of event
        data_string = json.dumps(data)

        # push to event method
        user_subscription(data_string)

        # have we injected?
        subscriptions = FactServicesStorefrontSubscription.objects.all()
        client = DimensionClient.objects.get(client_id=c_id)
        platform = DimensionPlatform.objects.get(
            os='iOS',
            name='test-ios-platform',
            version='7.1.0'
        )
        state = DimensionSubscriptionState.objects.get(state=0)
        status = DimensionSubscriptionStatus.objects.get(id=0)
        sub_type = DimensionSubscriptionType.objects.get(period='P1M', recurrence=1)
        territory = DimensionTerritory.objects.get(code='GB')
        utc_date = DimensionUTCDate.date_from_datetime(datetime=str(when))
        user = DimensionUser.objects.get(
            internal_user_id=i_uid,
            external_user_id=e_uid,
            territory=territory,
            client=client
        )

        # lets check to see if we have our subscription
        assert_that(subscriptions, has_length(1))

        # is it.. our subscription?
        assert_that(
            subscriptions[0],
            has_properties(
                subscription_id=sub_id,
                user_id=user.id,
                platform=platform,
                subscription_type=sub_type,
                subscription_status=status,
                subscription_state=state,
                event_utc_date=utc_date,
                event_utc_datetime=when
            )
        )

        # as a bonus feature...
        # we created a non-registered client.. we should have flagged this error...
        # we also created a non-registered usage right.. we should have flagged this error too...
        # and lastly we also created a non-registered product.. we will also flag this.

        # fetch the flags
        flags = Flags.objects.all()
        # do we have them? we should have 3 flags
        assert_that(flags, has_length(3))

