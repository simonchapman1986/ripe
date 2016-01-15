from django.core.management.base import BaseCommand
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

import gc

import logging
log = logging.getLogger('reporting')


class Command(BaseCommand):

    help = 'Run an OLAP immediately'

    def handle(self, *args, **options):

        self.stdout.write(u'Starting OLAP process')

        exceptions = 0
        try:
            log.debug("Starting: fact_subscription aggregation")
            subscriptions.cube_subscriptions_daily.delay()
        except Exception as e:
            exceptions += 1
            self.stdout.write(u'Warning: {0} Cube failure ({1})'.format('Subscriptions', e.message))
            log.exception('')

        try:
            log.info("Starting: fact_registration aggregation")
            registrations.cube_registrations_daily.delay()
        except Exception as e:
            exceptions += 1
            self.stdout.write(u'Warning: {0} Cube failure ({1})'.format('Registrations', e.message))
            log.exception('')

        try:
            log.debug("Starting: fact_plays aggregation")
            plays.cube_plays_by_item_daily.delay()
        except Exception as e:
            exceptions += 1
            self.stdout.write(u'Warning: {0} Cube failure ({1})'.format('Plays', e.message))
            log.exception('')

        try:
            log.debug("Starting: download aggregation")
            download.cube_download_daily.delay()
        except Exception as e:
            exceptions += 1
            self.stdout.write(u'Warning: {0} Cube failure ({1})'.format('Download Daily', e.message))
            log.exception('')

        try:
            log.debug("Starting: storetransaction aggregation")
            storetransaction.cube_storetransaction_daily.delay()
        except Exception as e:
            exceptions += 1
            self.stdout.write(u'Warning: {0} Cube failure ({1})'.format('Store Transactions', e.message))
            log.exception('')

        try:
            log.debug("Starting: content aggregation")
            content.cube_content_daily.delay()
        except Exception as e:
            exceptions += 1
            self.stdout.write(u'Warning: {0} Cube failure ({1})'.format('Content Views', e.message))
            log.exception('')

        try:
            log.debug("Starting: subscription revenue")
            subscription_revenue.cube_subscription_revenue_daily.delay()
        except Exception as e:
            exceptions += 1
            self.stdout.write(u'Warning: {0} Cube failure ({1})'.format('Subscribed Users', e.message))
            log.exception('')

        try:
            log.debug("Starting: license delivery raw")
            license_delivery_raw.cube_licensing_delivery_raw_daily.delay()
        except Exception as e:
            exceptions += 1
            self.stdout.write(u'Warning: {0} Cube failure ({1})'.format('License Delivery', e.message))
            log.exception('')

        try:
            log.debug("Starting: Asset Match")
            asset_match.cube_asset_match_daily.delay()
        except Exception as e:
            exceptions += 1
            self.stdout.write(u'Warning: {0} Cube failure ({1})'.format('Asset Match', e.message))
            log.exception('')

        try:
            log.debug("Starting: registrations raw")
            registration_raw.cube_registrations_raw_daily.delay()
        except Exception as e:
            exceptions += 1
            self.stdout.write(u'Warning: {0} Cube failure ({1})'.format('Registered Users', e.message))
            log.exception('')

        gc.collect()
        self.stdout.write(u'Completed with {0} failures/warnings'.format(exceptions))




