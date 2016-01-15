import logging

from celery.task import periodic_task
from django.conf import settings

from apps.cubes.tasks.daily import subscriptions
from apps.cubes.tasks.daily import registrations
from apps.cubes.tasks.daily import plays
from apps.cubes.tasks.daily import download
from apps.cubes.tasks.daily import storetransaction
from apps.cubes.tasks.daily import content
from apps.cubes.tasks.daily import subscription_revenue
from apps.cubes.tasks.daily import license_delivery_raw
from apps.cubes.tasks.daily import asset_match
from apps.cubes.tasks.daily import registration_raw


logger = logging.getLogger('reporting')


@periodic_task(run_every=settings.AGGREGATE_FACTS_WHEN)
def aggregate_facts():
    logger.debug("Starting: fact_subscription aggregation")
    subscriptions.cube_subscriptions_daily.delay()

    logger.debug("Starting: fact_registration aggregation")
    registrations.cube_registrations_daily.delay()

    logger.debug("Starting: fact_plays aggregation")
    plays.cube_plays_by_item_daily.delay()

    logger.debug("Starting: download aggregation")
    download.cube_download_daily.delay()

    logger.debug("Starting: storetransaction aggregation")
    storetransaction.cube_storetransaction_daily.delay()

    logger.debug("Starting: content aggregation")
    content.cube_content_daily.delay()

    logger.debug("Starting: subscription revenue")
    subscription_revenue.cube_subscription_revenue_daily.delay()

    logger.debug("Starting: license delivery raw")
    license_delivery_raw.cube_licensing_delivery_raw_daily.delay()

    logger.debug("Starting: Asset Match")
    asset_match.cube_asset_match_daily.delay()

    logger.debug("Starting: registrations raw")
    registration_raw.cube_registrations_raw_daily.delay()