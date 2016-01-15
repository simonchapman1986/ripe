# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

from apps.cubes.migration_helpers.indexes import BuildIndexes
from apps.cubes.migration_helpers.indexes import BTREE
from apps.cubes.migration_helpers.indexes import HASH

from apps.cubes.migration_helpers.execute_many import execute_many


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CubeSubscriptionsDaily'
        db.create_table('summary_subscriptions_daily', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 21, 0, 0), auto_now=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('territory_code', self.gf('django.db.models.fields.CharField')(default='', max_length=10)),
            ('client_id', self.gf('django.db.models.fields.CharField')(default='', max_length=36)),
            ('window_item_id', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('window_product_id', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('window_pricing_id', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('window_usage_right_id', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('window_tier', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('window_type', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('window_on_going', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('window_repeat_count', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('window_auto_upgrade', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('window_allow_repurchase', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('subscription_status', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('subscription_state', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('subscription_state_error', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('year', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('month', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('day', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('day_of_week', self.gf('django.db.models.fields.IntegerField')()),
            ('day_name', self.gf('django.db.models.fields.CharField')(max_length=9)),
            ('week_of_year', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('quarter', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('os', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('version', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('total', self.gf('django.db.models.fields.IntegerField')()),
            ('total_new', self.gf('django.db.models.fields.IntegerField')()),
            ('average_per_day', self.gf('django.db.models.fields.IntegerField')()),
            ('change', self.gf('django.db.models.fields.IntegerField')()),
            ('breakdown_pct', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('cubes', ['CubeSubscriptionsDaily'])

        # Adding model 'CubeRegistrationsDaily'
        db.create_table('summary_registrations_daily', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 21, 0, 0), auto_now=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('territory_code', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('client_id', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('year', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('month', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('day', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('day_of_week', self.gf('django.db.models.fields.IntegerField')()),
            ('day_name', self.gf('django.db.models.fields.CharField')(max_length=9)),
            ('week_of_year', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('quarter', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('platform_os', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('platform_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('platform_version', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('device_os', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('device_model', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('device_make', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('device_os_version', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('total', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('total_new', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('average_per_day', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('change', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('breakdown_pct', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('cubes', ['CubeRegistrationsDaily'])

        # Adding model 'CubePlaysByItem'
        db.create_table('summary_plays_by_item_daily', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 21, 0, 0), auto_now=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('year', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('month', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('day', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('day_of_week', self.gf('django.db.models.fields.IntegerField')()),
            ('day_name', self.gf('django.db.models.fields.CharField')(max_length=9)),
            ('week_of_year', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('quarter', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('item_id', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('territory_code', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('client_id', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('device_id', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('metadata_id', self.gf('django.db.models.fields.CharField')(default='', max_length=255, null=True, blank=True)),
            ('item_title', self.gf('django.db.models.fields.CharField')(default='', max_length=255, null=True, blank=True)),
            ('item_provider_name', self.gf('django.db.models.fields.CharField')(default='', max_length=128L, null=True, blank=True)),
            ('item_isan', self.gf('django.db.models.fields.CharField')(default='', max_length=36, null=True, blank=True)),
            ('item_eidr', self.gf('django.db.models.fields.CharField')(default='', max_length=36, null=True, blank=True)),
            ('item_genres', self.gf('django.db.models.fields.TextField')(default='{}', blank=True)),
            ('item_release_date', self.gf('django.db.models.fields.CharField')(default='', max_length=24, null=True, blank=True)),
            ('item_production_company', self.gf('django.db.models.fields.CharField')(default='', max_length=128, null=True, blank=True)),
            ('item_release_year', self.gf('django.db.models.fields.CharField')(default='', max_length=16, null=True, blank=True)),
            ('item_primary_language', self.gf('django.db.models.fields.CharField')(default='', max_length=8)),
            ('item_runtime', self.gf('django.db.models.fields.CharField')(default='', max_length=8, null=True, blank=True)),
            ('item_vendor_name', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('item_episode_number', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('item_season', self.gf('django.db.models.fields.CharField')(default='', max_length=255, null=True, blank=True)),
            ('item_show_title', self.gf('django.db.models.fields.CharField')(default='', max_length=255, null=True, blank=True)),
            ('item_ultraviolet', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('total_new', self.gf('django.db.models.fields.IntegerField')()),
            ('total', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('cubes', ['CubePlaysByItem'])

        # Adding model 'CubeDownload'
        db.create_table('summary_download_daily', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 21, 0, 0), auto_now=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('territory_code', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('client_id', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('year', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('month', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('day', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('day_of_week', self.gf('django.db.models.fields.IntegerField')()),
            ('day_name', self.gf('django.db.models.fields.CharField')(max_length=9)),
            ('week_of_year', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('quarter', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('product_id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('asset_id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('network', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('total', self.gf('django.db.models.fields.IntegerField')()),
            ('total_new', self.gf('django.db.models.fields.IntegerField')()),
            ('average_per_day', self.gf('django.db.models.fields.IntegerField')()),
            ('breakdown_pct', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('cubes', ['CubeDownload'])

        # Adding model 'CubeStoreTransaction'
        db.create_table('summary_storetransaction_daily', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 21, 0, 0), auto_now=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('territory_code', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('client_id', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('year', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('month', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('day', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('day_of_week', self.gf('django.db.models.fields.IntegerField')()),
            ('day_name', self.gf('django.db.models.fields.CharField')(max_length=9)),
            ('week_of_year', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('quarter', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('item_id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('window_id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('product_id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('transaction_status', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('right_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('currency_code', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('retail_model', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('definition', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('device_id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('platform_os', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('platform_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('platform_version', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('mnc', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('mcc', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('total', self.gf('django.db.models.fields.IntegerField')()),
            ('total_new', self.gf('django.db.models.fields.IntegerField')()),
            ('average_per_day', self.gf('django.db.models.fields.IntegerField')()),
            ('breakdown_pct', self.gf('django.db.models.fields.IntegerField')()),
            ('total_price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2)),
            ('total_price_day', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2)),
        ))
        db.send_create_signal('cubes', ['CubeStoreTransaction'])

        # Adding model 'CubeContent'
        db.create_table('summary_content_daily', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 21, 0, 0), auto_now=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('client_id', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('content_provider', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('asset_role_type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('mezzanine_delivery_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('definition', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('year', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('month', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('day', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('day_of_week', self.gf('django.db.models.fields.IntegerField')()),
            ('day_name', self.gf('django.db.models.fields.CharField')(max_length=9)),
            ('week_of_year', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('quarter', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('file_size', self.gf('django.db.models.fields.BigIntegerField')(max_length=10)),
            ('duration_of_asset', self.gf('django.db.models.fields.IntegerField')(default='', max_length=10)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('added_to_client', self.gf('django.db.models.fields.DateField')(null=True)),
        ))
        db.send_create_signal('cubes', ['CubeContent'])

        # Adding model 'Log'
        db.create_table('log', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cube', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('date', self.gf('django.db.models.fields.DateField')(default=None)),
            ('time_taken', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=7, decimal_places=6)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
        ))
        db.send_create_signal('cubes', ['Log'])

        # Adding unique constraint on 'Log', fields ['cube', 'date']
        db.create_unique('log', ['cube', 'date'])

        # Build all indexes
        # subscription indexes
        dbi = BuildIndexes(db_name='summary_subscriptions_daily')

        # HASH indexes
        dbi.create_index(field_name='territory_code', index_type=HASH)
        dbi.create_index(field_name='client_id', index_type=HASH)
        dbi.create_index(field_name='window_item_id', index_type=HASH)
        dbi.create_index(field_name='window_pricing_id', index_type=HASH)
        dbi.create_index(field_name='window_usage_right_id', index_type=HASH)
        dbi.create_index(field_name='window_tier', index_type=HASH)
        dbi.create_index(field_name='window_type', index_type=HASH)
        dbi.create_index(field_name='window_on_going', index_type=HASH)
        dbi.create_index(field_name='window_repeat_count', index_type=HASH)
        dbi.create_index(field_name='window_auto_upgrade', index_type=HASH)
        dbi.create_index(field_name='window_allow_repurchase', index_type=HASH)
        dbi.create_index(field_name='os', index_type=HASH)
        dbi.create_index(field_name='name', index_type=HASH)
        dbi.create_index(field_name='version', index_type=HASH)
        dbi.create_index(field_name='subscription_state', index_type=HASH)
        dbi.create_index(field_name='subscription_state_error', index_type=HASH)
        dbi.create_index(field_name='subscription_status', index_type=HASH)

        # date indexes BTREE
        dbi.create_index(field_name='date', index_type=BTREE)
        dbi.create_index(field_name='year', index_type=BTREE)
        dbi.create_index(field_name='month', index_type=BTREE)
        dbi.create_index(field_name='day', index_type=BTREE)
        dbi.create_index(field_name='day_of_week', index_type=BTREE)
        dbi.create_index(field_name='week_of_year', index_type=BTREE)
        dbi.create_index(field_name='day_name', index_type=BTREE)
        dbi.create_index(field_name='quarter', index_type=BTREE)
        dbi.create_index(field_name='created', index_type=BTREE)

        execute_many(db, str(dbi))

        # registration indexes
        dbi = BuildIndexes(db_name='summary_registrations_daily')

        # HASH indexes
        dbi.create_index(field_name='territory_code', index_type=HASH)
        dbi.create_index(field_name='client_id', index_type=HASH)
        dbi.create_index(field_name='platform_os', index_type=HASH)
        dbi.create_index(field_name='platform_name', index_type=HASH)
        dbi.create_index(field_name='platform_version', index_type=HASH)
        dbi.create_index(field_name='device_os', index_type=HASH)
        dbi.create_index(field_name='device_model', index_type=HASH)
        dbi.create_index(field_name='device_make', index_type=HASH)
        dbi.create_index(field_name='device_os_version', index_type=HASH)

        # date indexes BTREE
        dbi.create_index(field_name='date', index_type=BTREE)
        dbi.create_index(field_name='year', index_type=BTREE)
        dbi.create_index(field_name='month', index_type=BTREE)
        dbi.create_index(field_name='day', index_type=BTREE)
        dbi.create_index(field_name='day_of_week', index_type=BTREE)
        dbi.create_index(field_name='week_of_year', index_type=BTREE)
        dbi.create_index(field_name='day_name', index_type=BTREE)
        dbi.create_index(field_name='quarter', index_type=BTREE)
        dbi.create_index(field_name='created', index_type=BTREE)

        execute_many(db, str(dbi))

        # plays daily indexes
        dbi = BuildIndexes(db_name='summary_plays_by_item_daily')

        # HASH indexes
        dbi.create_index(field_name='territory_code', index_type=HASH)
        dbi.create_index(field_name='client_id', index_type=HASH)
        dbi.create_index(field_name='item_id', index_type=HASH)
        dbi.create_index(field_name='device_id', index_type=HASH)
        dbi.create_index(field_name='status', index_type=HASH)
        dbi.create_index(field_name='metadata_id', index_type=HASH)
        dbi.create_index(field_name='item_title', index_type=HASH)
        dbi.create_index(field_name='item_provider_name', index_type=HASH)
        dbi.create_index(field_name='item_isan', index_type=HASH)
        dbi.create_index(field_name='item_eidr', index_type=HASH)
        dbi.create_index(field_name='item_release_date', index_type=HASH)
        dbi.create_index(field_name='item_production_company', index_type=HASH)
        dbi.create_index(field_name='item_release_year', index_type=HASH)
        dbi.create_index(field_name='item_primary_language', index_type=HASH)
        dbi.create_index(field_name='item_runtime', index_type=HASH)
        dbi.create_index(field_name='item_vendor_name', index_type=HASH)
        dbi.create_index(field_name='item_episode_number', index_type=HASH)
        dbi.create_index(field_name='item_season', index_type=HASH)
        dbi.create_index(field_name='item_show_title', index_type=HASH)
        dbi.create_index(field_name='item_ultraviolet', index_type=HASH)

        # date indexes BTREE
        dbi.create_index(field_name='date', index_type=BTREE)
        dbi.create_index(field_name='year', index_type=BTREE)
        dbi.create_index(field_name='month', index_type=BTREE)
        dbi.create_index(field_name='day', index_type=BTREE)
        dbi.create_index(field_name='day_of_week', index_type=BTREE)
        dbi.create_index(field_name='week_of_year', index_type=BTREE)
        dbi.create_index(field_name='day_name', index_type=BTREE)
        dbi.create_index(field_name='quarter', index_type=BTREE)
        dbi.create_index(field_name='created', index_type=BTREE)

        execute_many(db, str(dbi))

        # download indexes
        dbi = BuildIndexes(db_name='summary_download_daily')

        # HASH indexes
        dbi.create_index(field_name='territory_code', index_type=HASH)
        dbi.create_index(field_name='client_id', index_type=HASH)
        dbi.create_index(field_name='product_id', index_type=HASH)
        dbi.create_index(field_name='asset_id', index_type=HASH)
        dbi.create_index(field_name='status', index_type=HASH)
        dbi.create_index(field_name='network', index_type=HASH)

        # date indexes BTREE
        dbi.create_index(field_name='date', index_type=BTREE)
        dbi.create_index(field_name='year', index_type=BTREE)
        dbi.create_index(field_name='month', index_type=BTREE)
        dbi.create_index(field_name='day', index_type=BTREE)
        dbi.create_index(field_name='day_of_week', index_type=BTREE)
        dbi.create_index(field_name='week_of_year', index_type=BTREE)
        dbi.create_index(field_name='day_name', index_type=BTREE)
        dbi.create_index(field_name='quarter', index_type=BTREE)
        dbi.create_index(field_name='created', index_type=BTREE)

        execute_many(db, str(dbi))

        # store transaction build
        dbi = BuildIndexes(db_name='summary_storetransaction_daily')

        # HASH indexes
        dbi.create_index(field_name='territory_code', index_type=HASH)
        dbi.create_index(field_name='client_id', index_type=HASH)
        dbi.create_index(field_name='item_id', index_type=HASH)
        dbi.create_index(field_name='window_id', index_type=HASH)
        dbi.create_index(field_name='product_id', index_type=HASH)
        dbi.create_index(field_name='transaction_status', index_type=HASH)
        dbi.create_index(field_name='right_id', index_type=HASH)
        dbi.create_index(field_name='currency_code', index_type=HASH)
        dbi.create_index(field_name='retail_model', index_type=HASH)
        dbi.create_index(field_name='definition', index_type=HASH)
        dbi.create_index(field_name='device_id', index_type=HASH)
        dbi.create_index(field_name='mnc', index_type=HASH)
        dbi.create_index(field_name='mcc', index_type=HASH)
        dbi.create_index(field_name='platform_os', index_type=HASH)
        dbi.create_index(field_name='platform_name', index_type=HASH)
        dbi.create_index(field_name='platform_version', index_type=HASH)

        # date indexes BTREE
        dbi.create_index(field_name='date', index_type=BTREE)
        dbi.create_index(field_name='year', index_type=BTREE)
        dbi.create_index(field_name='month', index_type=BTREE)
        dbi.create_index(field_name='day', index_type=BTREE)
        dbi.create_index(field_name='day_of_week', index_type=BTREE)
        dbi.create_index(field_name='week_of_year', index_type=BTREE)
        dbi.create_index(field_name='day_name', index_type=BTREE)
        dbi.create_index(field_name='quarter', index_type=BTREE)
        dbi.create_index(field_name='created', index_type=BTREE)

        execute_many(db, str(dbi))

        # content build
        dbi = BuildIndexes(db_name='summary_content_daily')

        # HASH indexes
        dbi.create_index(field_name='client_id', index_type=HASH)
        dbi.create_index(field_name='content_provider', index_type=HASH)
        dbi.create_index(field_name='asset_role_type', index_type=HASH)
        dbi.create_index(field_name='mezzanine_delivery_date', index_type=BTREE)
        dbi.create_index(field_name='definition', index_type=HASH)
        dbi.create_index(field_name='language', index_type=HASH)
        dbi.create_index(field_name='file_size', index_type=BTREE)
        dbi.create_index(field_name='duration_of_asset', index_type=BTREE)
        dbi.create_index(field_name='title', index_type=HASH)
        dbi.create_index(field_name='added_to_client', index_type=BTREE)

        # date indexes BTREE
        dbi.create_index(field_name='date', index_type=BTREE)
        dbi.create_index(field_name='year', index_type=BTREE)
        dbi.create_index(field_name='month', index_type=BTREE)
        dbi.create_index(field_name='day', index_type=BTREE)
        dbi.create_index(field_name='day_of_week', index_type=BTREE)
        dbi.create_index(field_name='week_of_year', index_type=BTREE)
        dbi.create_index(field_name='day_name', index_type=BTREE)
        dbi.create_index(field_name='quarter', index_type=BTREE)
        dbi.create_index(field_name='created', index_type=BTREE)

        execute_many(db, str(dbi))

    def backwards(self, orm):
        # Removing unique constraint on 'Log', fields ['cube', 'date']
        db.delete_unique('log', ['cube', 'date'])

        # Deleting model 'CubeSubscriptionsDaily'
        db.delete_table('summary_subscriptions_daily')

        # Deleting model 'CubeRegistrationsDaily'
        db.delete_table('summary_registrations_daily')

        # Deleting model 'CubePlaysByItem'
        db.delete_table('summary_plays_by_item_daily')

        # Deleting model 'CubeDownload'
        db.delete_table('summary_download_daily')

        # Deleting model 'CubeStoreTransaction'
        db.delete_table('summary_storetransaction_daily')

        # Deleting model 'CubeContent'
        db.delete_table('summary_content_daily')

        # Deleting model 'Log'
        db.delete_table('log')


    models = {
        'cubes.cubecontent': {
            'Meta': {'object_name': 'CubeContent', 'db_table': "'summary_content_daily'"},
            'added_to_client': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'asset_role_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'client_id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'content_provider': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 21, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'day': ('django.db.models.fields.SmallIntegerField', [], {}),
            'day_name': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'day_of_week': ('django.db.models.fields.IntegerField', [], {}),
            'definition': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'duration_of_asset': ('django.db.models.fields.IntegerField', [], {'default': "''", 'max_length': '10'}),
            'file_size': ('django.db.models.fields.BigIntegerField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'mezzanine_delivery_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'month': ('django.db.models.fields.SmallIntegerField', [], {}),
            'quarter': ('django.db.models.fields.SmallIntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'week_of_year': ('django.db.models.fields.SmallIntegerField', [], {}),
            'year': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        'cubes.cubedownload': {
            'Meta': {'object_name': 'CubeDownload', 'db_table': "'summary_download_daily'"},
            'asset_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'average_per_day': ('django.db.models.fields.IntegerField', [], {}),
            'breakdown_pct': ('django.db.models.fields.IntegerField', [], {}),
            'client_id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 21, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'day': ('django.db.models.fields.SmallIntegerField', [], {}),
            'day_name': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'day_of_week': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'month': ('django.db.models.fields.SmallIntegerField', [], {}),
            'network': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'product_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'quarter': ('django.db.models.fields.SmallIntegerField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'territory_code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'total': ('django.db.models.fields.IntegerField', [], {}),
            'total_new': ('django.db.models.fields.IntegerField', [], {}),
            'week_of_year': ('django.db.models.fields.SmallIntegerField', [], {}),
            'year': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        'cubes.cubeplaysbyitem': {
            'Meta': {'object_name': 'CubePlaysByItem', 'db_table': "'summary_plays_by_item_daily'"},
            'client_id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 21, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'day': ('django.db.models.fields.SmallIntegerField', [], {}),
            'day_name': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'day_of_week': ('django.db.models.fields.IntegerField', [], {}),
            'device_id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'item_eidr': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'item_episode_number': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'item_genres': ('django.db.models.fields.TextField', [], {'default': "'{}'", 'blank': 'True'}),
            'item_id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'item_isan': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'item_primary_language': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '8'}),
            'item_production_company': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'item_provider_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128L', 'null': 'True', 'blank': 'True'}),
            'item_release_date': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '24', 'null': 'True', 'blank': 'True'}),
            'item_release_year': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'item_runtime': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'item_season': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'item_show_title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'item_title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'item_ultraviolet': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'item_vendor_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'metadata_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'month': ('django.db.models.fields.SmallIntegerField', [], {}),
            'quarter': ('django.db.models.fields.SmallIntegerField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'territory_code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'total': ('django.db.models.fields.IntegerField', [], {}),
            'total_new': ('django.db.models.fields.IntegerField', [], {}),
            'week_of_year': ('django.db.models.fields.SmallIntegerField', [], {}),
            'year': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        'cubes.cuberegistrationsdaily': {
            'Meta': {'object_name': 'CubeRegistrationsDaily', 'db_table': "'summary_registrations_daily'"},
            'average_per_day': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'breakdown_pct': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'change': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'client_id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 21, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'day': ('django.db.models.fields.SmallIntegerField', [], {}),
            'day_name': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'day_of_week': ('django.db.models.fields.IntegerField', [], {}),
            'device_make': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'device_model': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'device_os': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'device_os_version': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'month': ('django.db.models.fields.SmallIntegerField', [], {}),
            'platform_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'platform_os': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'platform_version': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'quarter': ('django.db.models.fields.SmallIntegerField', [], {}),
            'territory_code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'total': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'total_new': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'week_of_year': ('django.db.models.fields.SmallIntegerField', [], {}),
            'year': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        'cubes.cubestoretransaction': {
            'Meta': {'object_name': 'CubeStoreTransaction', 'db_table': "'summary_storetransaction_daily'"},
            'average_per_day': ('django.db.models.fields.IntegerField', [], {}),
            'breakdown_pct': ('django.db.models.fields.IntegerField', [], {}),
            'client_id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 21, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'currency_code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'day': ('django.db.models.fields.SmallIntegerField', [], {}),
            'day_name': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'day_of_week': ('django.db.models.fields.IntegerField', [], {}),
            'definition': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'device_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'item_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'mcc': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'mnc': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'month': ('django.db.models.fields.SmallIntegerField', [], {}),
            'platform_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'platform_os': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'platform_version': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'product_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'quarter': ('django.db.models.fields.SmallIntegerField', [], {}),
            'retail_model': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'right_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'territory_code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'total': ('django.db.models.fields.IntegerField', [], {}),
            'total_new': ('django.db.models.fields.IntegerField', [], {}),
            'total_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2'}),
            'total_price_day': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2'}),
            'transaction_status': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'week_of_year': ('django.db.models.fields.SmallIntegerField', [], {}),
            'window_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'year': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        'cubes.cubesubscriptionsdaily': {
            'Meta': {'object_name': 'CubeSubscriptionsDaily', 'db_table': "'summary_subscriptions_daily'"},
            'average_per_day': ('django.db.models.fields.IntegerField', [], {}),
            'breakdown_pct': ('django.db.models.fields.IntegerField', [], {}),
            'change': ('django.db.models.fields.IntegerField', [], {}),
            'client_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '36'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 21, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'day': ('django.db.models.fields.SmallIntegerField', [], {}),
            'day_name': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'day_of_week': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'month': ('django.db.models.fields.SmallIntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'os': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'quarter': ('django.db.models.fields.SmallIntegerField', [], {}),
            'subscription_state': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'subscription_state_error': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subscription_status': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'territory_code': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10'}),
            'total': ('django.db.models.fields.IntegerField', [], {}),
            'total_new': ('django.db.models.fields.IntegerField', [], {}),
            'version': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'week_of_year': ('django.db.models.fields.SmallIntegerField', [], {}),
            'window_allow_repurchase': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'window_auto_upgrade': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'window_item_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'window_on_going': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'window_pricing_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'window_product_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'window_repeat_count': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'window_tier': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'window_type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'window_usage_right_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'year': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        'cubes.log': {
            'Meta': {'unique_together': "(('cube', 'date'),)", 'object_name': 'Log', 'db_table': "'log'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'cube': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'None'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time_taken': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '7', 'decimal_places': '6'})
        }
    }

    complete_apps = ['cubes']