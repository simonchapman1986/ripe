from django.core.management.base import BaseCommand

from apps.cubes.tasks.daily.registrations import cube_registrations_daily
from apps.cubes.tasks.daily.subscriptions import cube_subscriptions_daily
from apps.cubes.tasks.daily.plays import cube_plays_by_item_daily
from apps.cubes.tasks.daily.download import cube_download_daily
from apps.cubes.tasks.daily.storetransaction import cube_storetransaction_daily
from apps.cubes.tasks.daily.subscription_revenue import cube_subscription_revenue_daily
from apps.cubes.tasks.daily.license_delivery_raw import cube_licensing_delivery_raw_daily
from apps.cubes.tasks.daily.asset_match import cube_asset_match_daily


class Command(BaseCommand):

    help = 'Run auto OLAP'

    def handle(self, *args, **options):

        self.stdout.write(u'Starting OLAP process')



        self.stdout.write(u'Completed with {0} failures/warnings'.format(i))
