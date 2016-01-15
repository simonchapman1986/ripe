# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DimensionPlatform'
        db.create_table('dim_platform', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('os', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('base', ['DimensionPlatform'])

        # Adding unique constraint on 'DimensionPlatform', fields ['os', 'name', 'version']
        db.create_unique('dim_platform', ['os', 'name', 'version'])

        # Adding model 'DimensionSubscriptionStatus'
        db.create_table('dim_subscription_status', (
            ('id', self.gf('django.db.models.fields.IntegerField')(default=1, primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(default='unknown', max_length=20)),
        ))
        db.send_create_signal('base', ['DimensionSubscriptionStatus'])

        # Adding model 'DimensionUTCDate'
        db.create_table('dim_utc_date', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('year', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('month', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('day', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('day_of_week', self.gf('django.db.models.fields.IntegerField')()),
            ('day_name', self.gf('django.db.models.fields.CharField')(max_length=9)),
            ('week_of_year', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('quarter', self.gf('django.db.models.fields.SmallIntegerField')()),
        ))
        db.send_create_signal('base', ['DimensionUTCDate'])

        # Adding model 'DimensionSubscriptionState'
        db.create_table('dim_subscription_state', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('state', self.gf('django.db.models.fields.CharField')(default='unknown', unique=True, max_length=255)),
        ))
        db.send_create_signal('base', ['DimensionSubscriptionState'])

        # Adding model 'DimensionSubscriptionType'
        db.create_table('dim_subscription_type', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('period', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('recurrence', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('base', ['DimensionSubscriptionType'])

        # Adding unique constraint on 'DimensionSubscriptionType', fields ['period', 'recurrence']
        db.create_unique('dim_subscription_type', ['period', 'recurrence'])

        # Adding model 'Clients'
        db.create_table('clients', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('ftp_client_dir', self.gf('django.db.models.fields.CharField')(default='default', max_length=255)),
        ))
        db.send_create_signal('base', ['Clients'])

        # Adding model 'DimensionClient'
        db.create_table('dim_client', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=36, blank=True)),
        ))
        db.send_create_signal('base', ['DimensionClient'])

        # Adding model 'DimensionTerritory'
        db.create_table('dim_territory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=10)),
        ))
        db.send_create_signal('base', ['DimensionTerritory'])

        # Adding model 'DimensionUser'
        db.create_table('dim_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('internal_user_id', self.gf('django.db.models.fields.CharField')(default='00000000-0000-0000-0000-000000000000', max_length=36, blank=True)),
            ('external_user_id', self.gf('django.db.models.fields.CharField')(default='00000000-0000-0000-0000-000000000000', max_length=36, blank=True)),
            ('territory', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['base.DimensionTerritory'])),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['base.DimensionClient'])),
        ))
        db.send_create_signal('base', ['DimensionUser'])

        # Adding unique constraint on 'DimensionUser', fields ['internal_user_id', 'external_user_id', 'territory', 'client']
        db.create_unique('dim_user', ['internal_user_id', 'external_user_id', 'territory_id', 'client_id'])

        # Adding model 'DimensionItemProvider'
        db.create_table('dim_item_provider', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('provider_id', self.gf('django.db.models.fields.IntegerField')(unique=True, null=True, blank=True)),
            ('provider_name', self.gf('django.db.models.fields.CharField')(max_length=128L, unique=True, null=True, blank=True)),
        ))
        db.send_create_signal('base', ['DimensionItemProvider'])

        # Adding model 'DimensionItem'
        db.create_table('dim_item', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item_id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('content_type', self.gf('django.db.models.fields.CharField')(max_length=30L, null=True, blank=True)),
            ('item_title', self.gf('django.db.models.fields.CharField')(max_length=255L, null=True, blank=True)),
            ('release_year', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('item_runtime', self.gf('django.db.models.fields.CharField')(max_length=8L, null=True, blank=True)),
            ('item_duration', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('item_provider', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.DimensionItemProvider'], null=True, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('base', ['DimensionItem'])

        # Adding model 'DimensionProduct'
        db.create_table('dim_product', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('base', ['DimensionProduct'])

        # Adding model 'DimensionRight'
        db.create_table('dim_right', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('right_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('base', ['DimensionRight'])

        # Adding model 'DimensionWindow'
        db.create_table('dim_window', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('window_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('item_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('product_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('end_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('pricing_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('usage_right_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('tier', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('deleted', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('window_type', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('on_going', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('repeat_count', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=10)),
            ('auto_upgrade', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('allow_repurchase', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('apple_product_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
        ))
        db.send_create_signal('base', ['DimensionWindow'])

        # Adding model 'FactServicesStorefrontSubscription'
        db.create_table('fact_services_storefront_subscriptions', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['base.DimensionUser'])),
            ('subscription_id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('subscription_type', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['base.DimensionSubscriptionType'])),
            ('subscription_status', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['base.DimensionSubscriptionStatus'])),
            ('subscription_state', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['base.DimensionSubscriptionState'])),
            ('subscription_state_error', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('platform', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['base.DimensionPlatform'])),
            ('window', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['base.DimensionWindow'])),
            ('transaction_id', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('event_utc_date', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.DimensionUTCDate'])),
            ('event_utc_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('last_modified_utc', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('base', ['FactServicesStorefrontSubscription'])

        # Adding model 'DimensionDevice'
        db.create_table('dim_device', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('device_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=36, blank=True)),
            ('make', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('model', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('os', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('os_version', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('base', ['DimensionDevice'])

        # Adding unique constraint on 'DimensionDevice', fields ['os', 'make', 'model', 'os_version']
        db.create_unique('dim_device', ['os', 'make', 'model', 'os_version'])

        # Adding model 'FactServicesStorefrontRegistration'
        db.create_table('fact_services_storefront_registrations', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.DimensionUser'])),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.DimensionClient'])),
            ('platform', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['base.DimensionPlatform'])),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['base.DimensionDevice'])),
            ('event_utc_date', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.DimensionUTCDate'])),
            ('event_utc_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('last_modified_utc', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('base', ['FactServicesStorefrontRegistration'])

        # Adding model 'FactServicesStorefrontDownload'
        db.create_table('fact_services_storefront_download', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['base.DimensionItem'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['base.DimensionUser'])),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['base.DimensionDevice'])),
            ('product_id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('asset_id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('network', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('expiry_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('event_utc_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('event_utc_date', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.DimensionUTCDate'], null=True)),
            ('last_modified_utc', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('base', ['FactServicesStorefrontDownload'])

        # Adding model 'DimensionAccount'
        db.create_table('dim_account', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('account_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('base', ['DimensionAccount'])

        # Adding model 'DimensionRetailModel'
        db.create_table('dim_retail_model', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('model', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('base', ['DimensionRetailModel'])

        # Adding model 'DimensionDefinition'
        db.create_table('dim_definition', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('definition', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('base', ['DimensionDefinition'])

        # Adding model 'DimensionCurrency'
        db.create_table('dim_currency', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=10)),
        ))
        db.send_create_signal('base', ['DimensionCurrency'])

        # Adding model 'DimensionStoreTransactionStatus'
        db.create_table('dim_store_transaction_status', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(default='pending', max_length=20)),
        ))
        db.send_create_signal('base', ['DimensionStoreTransactionStatus'])

        # Adding model 'FactServicesStorefrontTransaction'
        db.create_table('fact_services_storefront_transaction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['base.DimensionItem'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['base.DimensionProduct'])),
            ('window', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['base.DimensionWindow'])),
            ('transaction_id', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('transaction_status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.DimensionStoreTransactionStatus'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['base.DimensionUser'])),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['base.DimensionAccount'])),
            ('right', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['base.DimensionRight'])),
            ('price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2)),
            ('currency', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['base.DimensionCurrency'])),
            ('retail_model', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['base.DimensionRetailModel'])),
            ('definition', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['base.DimensionDefinition'])),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['base.DimensionClient'])),
            ('territory', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['base.DimensionTerritory'])),
            ('platform', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['base.DimensionPlatform'])),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['base.DimensionDevice'])),
            ('mnc', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('mcc', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('event_utc_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('event_utc_date', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.DimensionUTCDate'], null=True)),
            ('last_modified_utc', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('base', ['FactServicesStorefrontTransaction'])

        # Adding model 'DimensionPlayStatus'
        db.create_table('dim_play_status', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='unknown', unique=True, max_length=20)),
        ))
        db.send_create_signal('base', ['DimensionPlayStatus'])

        # Adding model 'FactServicesHeartbeatPlayBuffer'
        db.create_table('fact_services_heartbeat_play_buffer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('duration', self.gf('django.db.models.fields.BigIntegerField')()),
            ('event_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('event_utc_date', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.DimensionUTCDate'], null=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
        ))
        db.send_create_signal('base', ['FactServicesHeartbeatPlayBuffer'])

        # Adding model 'FactServicesHeartbeatPlay'
        db.create_table('fact_services_heartbeat_plays', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item_id', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['base.DimensionItem'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['base.DimensionUser'])),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['base.DimensionDevice'])),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['base.DimensionPlayStatus'])),
            ('country_code', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['base.DimensionTerritory'])),
            ('event_utc_date', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.DimensionUTCDate'], null=True)),
            ('event_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('position', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
            ('bit_rate', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
        ))
        db.send_create_signal('base', ['FactServicesHeartbeatPlay'])

        # Adding M2M table for field play_buffer on 'FactServicesHeartbeatPlay'
        m2m_table_name = db.shorten_name('fact_services_heartbeat_plays_play_buffer')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('factservicesheartbeatplay', models.ForeignKey(orm['base.factservicesheartbeatplay'], null=False)),
            ('factservicesheartbeatplaybuffer', models.ForeignKey(orm['base.factservicesheartbeatplaybuffer'], null=False))
        ))
        db.create_unique(m2m_table_name, ['factservicesheartbeatplay_id', 'factservicesheartbeatplaybuffer_id'])

        # Adding model 'FactServicesHeartbeatPlayInit'
        db.create_table('fact_services_heartbeat_play_init', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('heartbeat', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['base.FactServicesHeartbeatPlay'])),
            ('duration', self.gf('django.db.models.fields.BigIntegerField')()),
            ('licensed', self.gf('django.db.models.fields.BooleanField')()),
            ('event_utc_date', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.DimensionUTCDate'], null=True)),
            ('event_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
        ))
        db.send_create_signal('base', ['FactServicesHeartbeatPlayInit'])

        # Adding model 'DimensionLanguage'
        db.create_table('dim_language', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('iso_code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=8)),
        ))
        db.send_create_signal('base', ['DimensionLanguage'])

        # Adding model 'DimensionVendor'
        db.create_table('dim_vendor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('base', ['DimensionVendor'])

        # Adding model 'DimensionMetadataType'
        db.create_table('dim_metadata_type', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('base', ['DimensionMetadataType'])

        # Adding model 'DimensionCountryCode'
        db.create_table('dim_metadata_country_code', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('iso_code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=2)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('base', ['DimensionCountryCode'])

        # Adding model 'FactServicesBackstageItemMetadata'
        db.create_table('fact_services_backstage_item_metadata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item_meta', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['base.DimensionItem'])),
            ('metadata_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('country_of_origin', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.DimensionCountryCode'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('copyright_cline', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('provider', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.DimensionItemProvider'], null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.DimensionMetadataType'])),
            ('isan', self.gf('django.db.models.fields.CharField')(max_length=36, null=True, blank=True)),
            ('eidr', self.gf('django.db.models.fields.CharField')(max_length=36, null=True, blank=True)),
            ('genres', self.gf('django.db.models.fields.TextField')(default='{}', blank=True)),
            ('release_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('production_company', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('release_year', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('primary_language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.DimensionLanguage'], null=True, blank=True)),
            ('short_synopsis', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('medium_synopsis', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('long_synopsis', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('runtime', self.gf('django.db.models.fields.CharField')(max_length=8, null=True, blank=True)),
            ('vendor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.DimensionVendor'])),
            ('episode_number', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('season', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('show_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=None)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=None)),
            ('original_url', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('ultraviolet', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('event_utc_date', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.DimensionUTCDate'])),
            ('event_utc_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('last_modified_utc', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('base', ['FactServicesBackstageItemMetadata'])

        # Adding model 'DimensionAssets'
        db.create_table('dim_assets', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('asset_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('base', ['DimensionAssets'])

        # Adding model 'DimensionDataRole'
        db.create_table('dim_data_role', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('role', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('base', ['DimensionDataRole'])

        # Adding model 'DimensionProcessingState'
        db.create_table('dim_processing_state', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('processing_state', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('base', ['DimensionProcessingState'])

        # Adding model 'FactServicesBackstageAssetMatch'
        db.create_table('fact_services_backstage_asset_match', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(related_name='matched_client', to=orm['base.DimensionClient'])),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(related_name='matched_item', to=orm['base.DimensionItem'])),
            ('asset', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, related_name='matched_asset', to=orm['base.DimensionAssets'])),
            ('data_role', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.DimensionDataRole'])),
            ('processing_state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.DimensionProcessingState'])),
            ('used_asset_ids', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('provider', self.gf('django.db.models.fields.related.ForeignKey')(related_name='matched_provider', to=orm['base.DimensionItemProvider'])),
            ('territory', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.DimensionTerritory'])),
            ('spec_name', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('delivery_date', self.gf('django.db.models.fields.DateTimeField')(default=None)),
            ('definition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.DimensionDefinition'])),
            ('file_size', self.gf('django.db.models.fields.BigIntegerField')(max_length=10)),
            ('duration', self.gf('django.db.models.fields.IntegerField')(default='', max_length=10)),
            ('event_date', self.gf('django.db.models.fields.DateField')(default=None)),
            ('event_utc_date', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.DimensionUTCDate'])),
            ('event_utc_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('last_modified_utc', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('base', ['FactServicesBackstageAssetMatch'])

        # Adding M2M table for field languages on 'FactServicesBackstageAssetMatch'
        m2m_table_name = db.shorten_name('fact_services_backstage_asset_match_languages')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('factservicesbackstageassetmatch', models.ForeignKey(orm['base.factservicesbackstageassetmatch'], null=False)),
            ('dimensionlanguage', models.ForeignKey(orm['base.dimensionlanguage'], null=False))
        ))
        db.create_unique(m2m_table_name, ['factservicesbackstageassetmatch_id', 'dimensionlanguage_id'])

        # Adding model 'DimensionJobManager'
        db.create_table('dim_job_manager', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('job_manager_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('base', ['DimensionJobManager'])

        # Adding model 'FactServicesPackagerPackage'
        db.create_table('fact_services_packager_package', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('job_manager_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.DimensionJobManager'])),
            ('item_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.DimensionItem'])),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('profile', self.gf('django.db.models.fields.TextField')()),
            ('event_utc_date', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.DimensionUTCDate'])),
            ('event_utc_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('last_modified_utc', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('base', ['FactServicesPackagerPackage'])

        # Adding M2M table for field asset_ids on 'FactServicesPackagerPackage'
        m2m_table_name = db.shorten_name('fact_services_packager_package_asset_ids')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('factservicespackagerpackage', models.ForeignKey(orm['base.factservicespackagerpackage'], null=False)),
            ('dimensionassets', models.ForeignKey(orm['base.dimensionassets'], null=False))
        ))
        db.create_unique(m2m_table_name, ['factservicespackagerpackage_id', 'dimensionassets_id'])

        # Adding model 'FactServicesEncoderEncode'
        db.create_table('fact_services_encoder_encode', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('job_manager_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.DimensionJobManager'])),
            ('item_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.DimensionItem'])),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('file_size', self.gf('django.db.models.fields.BigIntegerField')(max_length=10)),
            ('event_utc_date', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.DimensionUTCDate'])),
            ('event_utc_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('last_modified_utc', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('base', ['FactServicesEncoderEncode'])

        # Adding M2M table for field asset_ids on 'FactServicesEncoderEncode'
        m2m_table_name = db.shorten_name('fact_services_encoder_encode_asset_ids')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('factservicesencoderencode', models.ForeignKey(orm['base.factservicesencoderencode'], null=False)),
            ('dimensionassets', models.ForeignKey(orm['base.dimensionassets'], null=False))
        ))
        db.create_unique(m2m_table_name, ['factservicesencoderencode_id', 'dimensionassets_id'])

        # Adding model 'DimensionStudioItem'
        db.create_table('dim_studio_item', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('unique_studio_item_id', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
        ))
        db.send_create_signal('base', ['DimensionStudioItem'])

        # Adding model 'DimensionStudio'
        db.create_table('dim_studio', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('base', ['DimensionStudio'])

        # Adding model 'DimensionAudioChannels'
        db.create_table('dim_audio_channels', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('channel', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('base', ['DimensionAudioChannels'])

        # Adding model 'FactServicesAggregatorAggregation'
        db.create_table('fact_services_aggregator_aggregation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('asset', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['base.DimensionAssets'])),
            ('unique_studio_item', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['base.DimensionStudioItem'])),
            ('studio', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['base.DimensionStudio'])),
            ('file_name', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('file_size', self.gf('django.db.models.fields.BigIntegerField')(max_length=10)),
            ('checksum', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('data_role', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['base.DimensionDataRole'])),
            ('content_duration', self.gf('django.db.models.fields.IntegerField')(default='', max_length=10)),
            ('definition', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['base.DimensionDefinition'])),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['base.DimensionLanguage'])),
            ('audio_channel', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['base.DimensionAudioChannels'])),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['base.DimensionClient'])),
            ('vendor', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['base.DimensionVendor'])),
            ('event_utc_date', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.DimensionUTCDate'])),
            ('event_utc_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('last_modified_utc', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('base', ['FactServicesAggregatorAggregation'])

        # Adding model 'Config'
        db.create_table('config', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
        ))
        db.send_create_signal('base', ['Config'])

        # Adding model 'Service'
        db.create_table('service', (
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('access_key', self.gf('django.db.models.fields.CharField')(default='', unique=True, max_length=32)),
            ('access_secret', self.gf('django.db.models.fields.CharField')(default='', unique=True, max_length=32)),
        ))
        db.send_create_signal('base', ['Service'])


    def backwards(self, orm):
        # Removing unique constraint on 'DimensionDevice', fields ['os', 'make', 'model', 'os_version']
        db.delete_unique('dim_device', ['os', 'make', 'model', 'os_version'])

        # Removing unique constraint on 'DimensionUser', fields ['internal_user_id', 'external_user_id', 'territory', 'client']
        db.delete_unique('dim_user', ['internal_user_id', 'external_user_id', 'territory_id', 'client_id'])

        # Removing unique constraint on 'DimensionSubscriptionType', fields ['period', 'recurrence']
        db.delete_unique('dim_subscription_type', ['period', 'recurrence'])

        # Removing unique constraint on 'DimensionPlatform', fields ['os', 'name', 'version']
        db.delete_unique('dim_platform', ['os', 'name', 'version'])

        # Deleting model 'DimensionPlatform'
        db.delete_table('dim_platform')

        # Deleting model 'DimensionSubscriptionStatus'
        db.delete_table('dim_subscription_status')

        # Deleting model 'DimensionUTCDate'
        db.delete_table('dim_utc_date')

        # Deleting model 'DimensionSubscriptionState'
        db.delete_table('dim_subscription_state')

        # Deleting model 'DimensionSubscriptionType'
        db.delete_table('dim_subscription_type')

        # Deleting model 'Clients'
        db.delete_table('clients')

        # Deleting model 'DimensionClient'
        db.delete_table('dim_client')

        # Deleting model 'DimensionTerritory'
        db.delete_table('dim_territory')

        # Deleting model 'DimensionUser'
        db.delete_table('dim_user')

        # Deleting model 'DimensionItemProvider'
        db.delete_table('dim_item_provider')

        # Deleting model 'DimensionItem'
        db.delete_table('dim_item')

        # Deleting model 'DimensionProduct'
        db.delete_table('dim_product')

        # Deleting model 'DimensionRight'
        db.delete_table('dim_right')

        # Deleting model 'DimensionWindow'
        db.delete_table('dim_window')

        # Deleting model 'FactServicesStorefrontSubscription'
        db.delete_table('fact_services_storefront_subscriptions')

        # Deleting model 'DimensionDevice'
        db.delete_table('dim_device')

        # Deleting model 'FactServicesStorefrontRegistration'
        db.delete_table('fact_services_storefront_registrations')

        # Deleting model 'FactServicesStorefrontDownload'
        db.delete_table('fact_services_storefront_download')

        # Deleting model 'DimensionAccount'
        db.delete_table('dim_account')

        # Deleting model 'DimensionRetailModel'
        db.delete_table('dim_retail_model')

        # Deleting model 'DimensionDefinition'
        db.delete_table('dim_definition')

        # Deleting model 'DimensionCurrency'
        db.delete_table('dim_currency')

        # Deleting model 'DimensionStoreTransactionStatus'
        db.delete_table('dim_store_transaction_status')

        # Deleting model 'FactServicesStorefrontTransaction'
        db.delete_table('fact_services_storefront_transaction')

        # Deleting model 'DimensionPlayStatus'
        db.delete_table('dim_play_status')

        # Deleting model 'FactServicesHeartbeatPlayBuffer'
        db.delete_table('fact_services_heartbeat_play_buffer')

        # Deleting model 'FactServicesHeartbeatPlay'
        db.delete_table('fact_services_heartbeat_plays')

        # Removing M2M table for field play_buffer on 'FactServicesHeartbeatPlay'
        db.delete_table(db.shorten_name('fact_services_heartbeat_plays_play_buffer'))

        # Deleting model 'FactServicesHeartbeatPlayInit'
        db.delete_table('fact_services_heartbeat_play_init')

        # Deleting model 'DimensionLanguage'
        db.delete_table('dim_language')

        # Deleting model 'DimensionVendor'
        db.delete_table('dim_vendor')

        # Deleting model 'DimensionMetadataType'
        db.delete_table('dim_metadata_type')

        # Deleting model 'DimensionCountryCode'
        db.delete_table('dim_metadata_country_code')

        # Deleting model 'FactServicesBackstageItemMetadata'
        db.delete_table('fact_services_backstage_item_metadata')

        # Deleting model 'DimensionAssets'
        db.delete_table('dim_assets')

        # Deleting model 'DimensionDataRole'
        db.delete_table('dim_data_role')

        # Deleting model 'DimensionProcessingState'
        db.delete_table('dim_processing_state')

        # Deleting model 'FactServicesBackstageAssetMatch'
        db.delete_table('fact_services_backstage_asset_match')

        # Removing M2M table for field languages on 'FactServicesBackstageAssetMatch'
        db.delete_table(db.shorten_name('fact_services_backstage_asset_match_languages'))

        # Deleting model 'DimensionJobManager'
        db.delete_table('dim_job_manager')

        # Deleting model 'FactServicesPackagerPackage'
        db.delete_table('fact_services_packager_package')

        # Removing M2M table for field asset_ids on 'FactServicesPackagerPackage'
        db.delete_table(db.shorten_name('fact_services_packager_package_asset_ids'))

        # Deleting model 'FactServicesEncoderEncode'
        db.delete_table('fact_services_encoder_encode')

        # Removing M2M table for field asset_ids on 'FactServicesEncoderEncode'
        db.delete_table(db.shorten_name('fact_services_encoder_encode_asset_ids'))

        # Deleting model 'DimensionStudioItem'
        db.delete_table('dim_studio_item')

        # Deleting model 'DimensionStudio'
        db.delete_table('dim_studio')

        # Deleting model 'DimensionAudioChannels'
        db.delete_table('dim_audio_channels')

        # Deleting model 'FactServicesAggregatorAggregation'
        db.delete_table('fact_services_aggregator_aggregation')

        # Deleting model 'Config'
        db.delete_table('config')

        # Deleting model 'Service'
        db.delete_table('service')


    models = {
        'base.clients': {
            'Meta': {'object_name': 'Clients', 'db_table': "'clients'"},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'ftp_client_dir': ('django.db.models.fields.CharField', [], {'default': "'default'", 'max_length': '255'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        'base.config': {
            'Meta': {'object_name': 'Config', 'db_table': "'config'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'base.dimensionaccount': {
            'Meta': {'object_name': 'DimensionAccount', 'db_table': "'dim_account'"},
            'account_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'base.dimensionassets': {
            'Meta': {'object_name': 'DimensionAssets', 'db_table': "'dim_assets'"},
            'asset_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'base.dimensionaudiochannels': {
            'Meta': {'object_name': 'DimensionAudioChannels', 'db_table': "'dim_audio_channels'"},
            'channel': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'base.dimensionclient': {
            'Meta': {'object_name': 'DimensionClient', 'db_table': "'dim_client'"},
            'client_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '36', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'base.dimensioncountrycode': {
            'Meta': {'object_name': 'DimensionCountryCode', 'db_table': "'dim_metadata_country_code'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'base.dimensioncurrency': {
            'Meta': {'object_name': 'DimensionCurrency', 'db_table': "'dim_currency'"},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'base.dimensiondatarole': {
            'Meta': {'object_name': 'DimensionDataRole', 'db_table': "'dim_data_role'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'base.dimensiondefinition': {
            'Meta': {'object_name': 'DimensionDefinition', 'db_table': "'dim_definition'"},
            'definition': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'base.dimensiondevice': {
            'Meta': {'unique_together': "(('os', 'make', 'model', 'os_version'),)", 'object_name': 'DimensionDevice', 'db_table': "'dim_device'"},
            'device_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '36', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'make': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'os': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'os_version': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'base.dimensionitem': {
            'Meta': {'object_name': 'DimensionItem', 'db_table': "'dim_item'"},
            'content_type': ('django.db.models.fields.CharField', [], {'max_length': '30L', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_duration': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'item_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'item_provider': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.DimensionItemProvider']", 'null': 'True', 'blank': 'True'}),
            'item_runtime': ('django.db.models.fields.CharField', [], {'max_length': '8L', 'null': 'True', 'blank': 'True'}),
            'item_title': ('django.db.models.fields.CharField', [], {'max_length': '255L', 'null': 'True', 'blank': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'release_year': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'base.dimensionitemprovider': {
            'Meta': {'object_name': 'DimensionItemProvider', 'db_table': "'dim_item_provider'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'provider_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'provider_name': ('django.db.models.fields.CharField', [], {'max_length': '128L', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        'base.dimensionjobmanager': {
            'Meta': {'object_name': 'DimensionJobManager', 'db_table': "'dim_job_manager'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_manager_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'base.dimensionlanguage': {
            'Meta': {'object_name': 'DimensionLanguage', 'db_table': "'dim_language'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '8'})
        },
        'base.dimensionmetadatatype': {
            'Meta': {'object_name': 'DimensionMetadataType', 'db_table': "'dim_metadata_type'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'base.dimensionplatform': {
            'Meta': {'unique_together': "(('os', 'name', 'version'),)", 'object_name': 'DimensionPlatform', 'db_table': "'dim_platform'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'os': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'base.dimensionplaystatus': {
            'Meta': {'object_name': 'DimensionPlayStatus', 'db_table': "'dim_play_status'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'unknown'", 'unique': 'True', 'max_length': '20'})
        },
        'base.dimensionprocessingstate': {
            'Meta': {'object_name': 'DimensionProcessingState', 'db_table': "'dim_processing_state'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'processing_state': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'base.dimensionproduct': {
            'Meta': {'object_name': 'DimensionProduct', 'db_table': "'dim_product'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'base.dimensionretailmodel': {
            'Meta': {'object_name': 'DimensionRetailModel', 'db_table': "'dim_retail_model'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'base.dimensionright': {
            'Meta': {'object_name': 'DimensionRight', 'db_table': "'dim_right'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'right_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'base.dimensionstoretransactionstatus': {
            'Meta': {'object_name': 'DimensionStoreTransactionStatus', 'db_table': "'dim_store_transaction_status'"},
            'description': ('django.db.models.fields.CharField', [], {'default': "'pending'", 'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'base.dimensionstudio': {
            'Meta': {'object_name': 'DimensionStudio', 'db_table': "'dim_studio'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'base.dimensionstudioitem': {
            'Meta': {'object_name': 'DimensionStudioItem', 'db_table': "'dim_studio_item'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'unique_studio_item_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        },
        'base.dimensionsubscriptionstate': {
            'Meta': {'object_name': 'DimensionSubscriptionState', 'db_table': "'dim_subscription_state'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'unknown'", 'unique': 'True', 'max_length': '255'})
        },
        'base.dimensionsubscriptionstatus': {
            'Meta': {'object_name': 'DimensionSubscriptionStatus', 'db_table': "'dim_subscription_status'"},
            'description': ('django.db.models.fields.CharField', [], {'default': "'unknown'", 'max_length': '20'}),
            'id': ('django.db.models.fields.IntegerField', [], {'default': '1', 'primary_key': 'True'})
        },
        'base.dimensionsubscriptiontype': {
            'Meta': {'unique_together': "(('period', 'recurrence'),)", 'object_name': 'DimensionSubscriptionType', 'db_table': "'dim_subscription_type'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'period': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'recurrence': ('django.db.models.fields.IntegerField', [], {})
        },
        'base.dimensionterritory': {
            'Meta': {'object_name': 'DimensionTerritory', 'db_table': "'dim_territory'"},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'base.dimensionuser': {
            'Meta': {'unique_together': "(('internal_user_id', 'external_user_id', 'territory', 'client'),)", 'object_name': 'DimensionUser', 'db_table': "'dim_user'"},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': "orm['base.DimensionClient']"}),
            'external_user_id': ('django.db.models.fields.CharField', [], {'default': "'00000000-0000-0000-0000-000000000000'", 'max_length': '36', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_user_id': ('django.db.models.fields.CharField', [], {'default': "'00000000-0000-0000-0000-000000000000'", 'max_length': '36', 'blank': 'True'}),
            'territory': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': "orm['base.DimensionTerritory']"})
        },
        'base.dimensionutcdate': {
            'Meta': {'object_name': 'DimensionUTCDate', 'db_table': "'dim_utc_date'"},
            'date': ('django.db.models.fields.DateField', [], {}),
            'day': ('django.db.models.fields.SmallIntegerField', [], {}),
            'day_name': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'day_of_week': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'month': ('django.db.models.fields.SmallIntegerField', [], {}),
            'quarter': ('django.db.models.fields.SmallIntegerField', [], {}),
            'week_of_year': ('django.db.models.fields.SmallIntegerField', [], {}),
            'year': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        'base.dimensionvendor': {
            'Meta': {'object_name': 'DimensionVendor', 'db_table': "'dim_vendor'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'base.dimensionwindow': {
            'Meta': {'object_name': 'DimensionWindow', 'db_table': "'dim_window'"},
            'allow_repurchase': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'apple_product_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'auto_upgrade': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'deleted': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'on_going': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pricing_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'product_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'repeat_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '10'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'tier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'usage_right_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'window_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'window_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'})
        },
        'base.factservicesaggregatoraggregation': {
            'Meta': {'object_name': 'FactServicesAggregatorAggregation', 'db_table': "'fact_services_aggregator_aggregation'"},
            'asset': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': "orm['base.DimensionAssets']"}),
            'audio_channel': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': "orm['base.DimensionAudioChannels']"}),
            'checksum': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': "orm['base.DimensionClient']"}),
            'content_duration': ('django.db.models.fields.IntegerField', [], {'default': "''", 'max_length': '10'}),
            'data_role': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': "orm['base.DimensionDataRole']"}),
            'definition': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': "orm['base.DimensionDefinition']"}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {}),
            'event_utc_date': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.DimensionUTCDate']"}),
            'event_utc_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'file_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'file_size': ('django.db.models.fields.BigIntegerField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': "orm['base.DimensionLanguage']"}),
            'last_modified_utc': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {}),
            'studio': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': "orm['base.DimensionStudio']"}),
            'unique_studio_item': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': "orm['base.DimensionStudioItem']"}),
            'vendor': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': "orm['base.DimensionVendor']"})
        },
        'base.factservicesbackstageassetmatch': {
            'Meta': {'object_name': 'FactServicesBackstageAssetMatch', 'db_table': "'fact_services_backstage_asset_match'"},
            'asset': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'related_name': "'matched_asset'", 'to': "orm['base.DimensionAssets']"}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'matched_client'", 'to': "orm['base.DimensionClient']"}),
            'data_role': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.DimensionDataRole']"}),
            'definition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.DimensionDefinition']"}),
            'delivery_date': ('django.db.models.fields.DateTimeField', [], {'default': 'None'}),
            'duration': ('django.db.models.fields.IntegerField', [], {'default': "''", 'max_length': '10'}),
            'event_date': ('django.db.models.fields.DateField', [], {'default': 'None'}),
            'event_utc_date': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.DimensionUTCDate']"}),
            'event_utc_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'file_size': ('django.db.models.fields.BigIntegerField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'matched_item'", 'to': "orm['base.DimensionItem']"}),
            'languages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['base.DimensionLanguage']", 'symmetrical': 'False'}),
            'last_modified_utc': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'processing_state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.DimensionProcessingState']"}),
            'provider': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'matched_provider'", 'to': "orm['base.DimensionItemProvider']"}),
            'spec_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'territory': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.DimensionTerritory']"}),
            'used_asset_ids': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'})
        },
        'base.factservicesbackstageitemmetadata': {
            'Meta': {'object_name': 'FactServicesBackstageItemMetadata', 'db_table': "'fact_services_backstage_item_metadata'"},
            'copyright_cline': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'country_of_origin': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.DimensionCountryCode']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'None'}),
            'eidr': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'episode_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'event_utc_date': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.DimensionUTCDate']"}),
            'event_utc_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'genres': ('django.db.models.fields.TextField', [], {'default': "'{}'", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isan': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'item_meta': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': "orm['base.DimensionItem']"}),
            'last_modified_utc': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'long_synopsis': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'medium_synopsis': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'metadata_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'None'}),
            'original_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'primary_language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.DimensionLanguage']", 'null': 'True', 'blank': 'True'}),
            'production_company': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'provider': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.DimensionItemProvider']", 'null': 'True', 'blank': 'True'}),
            'release_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'release_year': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'runtime': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'season': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'short_synopsis': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'show_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.DimensionMetadataType']"}),
            'ultraviolet': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'vendor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.DimensionVendor']"}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'})
        },
        'base.factservicesencoderencode': {
            'Meta': {'object_name': 'FactServicesEncoderEncode', 'db_table': "'fact_services_encoder_encode'"},
            'asset_ids': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['base.DimensionAssets']", 'symmetrical': 'False'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {}),
            'event_utc_date': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.DimensionUTCDate']"}),
            'event_utc_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'file_size': ('django.db.models.fields.BigIntegerField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.DimensionItem']"}),
            'job_manager_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.DimensionJobManager']"}),
            'last_modified_utc': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {})
        },
        'base.factservicesheartbeatplay': {
            'Meta': {'object_name': 'FactServicesHeartbeatPlay', 'db_table': "'fact_services_heartbeat_plays'"},
            'bit_rate': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'country_code': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': "orm['base.DimensionTerritory']"}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': "orm['base.DimensionDevice']"}),
            'event_time': ('django.db.models.fields.DateTimeField', [], {}),
            'event_utc_date': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.DimensionUTCDate']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_id': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': "orm['base.DimensionItem']"}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'play_buffer': ('django.db.models.fields.related.ManyToManyField', [], {'default': '-1', 'to': "orm['base.FactServicesHeartbeatPlayBuffer']", 'symmetrical': 'False'}),
            'position': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': "orm['base.DimensionPlayStatus']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': "orm['base.DimensionUser']"})
        },
        'base.factservicesheartbeatplaybuffer': {
            'Meta': {'object_name': 'FactServicesHeartbeatPlayBuffer', 'db_table': "'fact_services_heartbeat_play_buffer'"},
            'duration': ('django.db.models.fields.BigIntegerField', [], {}),
            'event_time': ('django.db.models.fields.DateTimeField', [], {}),
            'event_utc_date': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.DimensionUTCDate']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'})
        },
        'base.factservicesheartbeatplayinit': {
            'Meta': {'object_name': 'FactServicesHeartbeatPlayInit', 'db_table': "'fact_services_heartbeat_play_init'"},
            'duration': ('django.db.models.fields.BigIntegerField', [], {}),
            'event_time': ('django.db.models.fields.DateTimeField', [], {}),
            'event_utc_date': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.DimensionUTCDate']", 'null': 'True'}),
            'heartbeat': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': "orm['base.FactServicesHeartbeatPlay']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'licensed': ('django.db.models.fields.BooleanField', [], {})
        },
        'base.factservicespackagerpackage': {
            'Meta': {'object_name': 'FactServicesPackagerPackage', 'db_table': "'fact_services_packager_package'"},
            'asset_ids': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['base.DimensionAssets']", 'symmetrical': 'False'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {}),
            'event_utc_date': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.DimensionUTCDate']"}),
            'event_utc_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.DimensionItem']"}),
            'job_manager_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.DimensionJobManager']"}),
            'last_modified_utc': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'profile': ('django.db.models.fields.TextField', [], {}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {})
        },
        'base.factservicesstorefrontdownload': {
            'Meta': {'object_name': 'FactServicesStorefrontDownload', 'db_table': "'fact_services_storefront_download'"},
            'asset_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': "orm['base.DimensionDevice']"}),
            'event_utc_date': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.DimensionUTCDate']", 'null': 'True'}),
            'event_utc_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': "orm['base.DimensionItem']"}),
            'last_modified_utc': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'network': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'product_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': "orm['base.DimensionUser']"})
        },
        'base.factservicesstorefrontregistration': {
            'Meta': {'object_name': 'FactServicesStorefrontRegistration', 'db_table': "'fact_services_storefront_registrations'"},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.DimensionClient']"}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': "orm['base.DimensionDevice']"}),
            'event_utc_date': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.DimensionUTCDate']"}),
            'event_utc_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified_utc': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'platform': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': "orm['base.DimensionPlatform']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.DimensionUser']"})
        },
        'base.factservicesstorefrontsubscription': {
            'Meta': {'object_name': 'FactServicesStorefrontSubscription', 'db_table': "'fact_services_storefront_subscriptions'"},
            'event_utc_date': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.DimensionUTCDate']"}),
            'event_utc_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified_utc': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'platform': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': "orm['base.DimensionPlatform']"}),
            'subscription_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'subscription_state': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': "orm['base.DimensionSubscriptionState']"}),
            'subscription_state_error': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'subscription_status': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': "orm['base.DimensionSubscriptionStatus']"}),
            'subscription_type': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': "orm['base.DimensionSubscriptionType']"}),
            'transaction_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': "orm['base.DimensionUser']"}),
            'window': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': "orm['base.DimensionWindow']"})
        },
        'base.factservicesstorefronttransaction': {
            'Meta': {'object_name': 'FactServicesStorefrontTransaction', 'db_table': "'fact_services_storefront_transaction'"},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': "orm['base.DimensionAccount']"}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': "orm['base.DimensionClient']"}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': "orm['base.DimensionCurrency']"}),
            'definition': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': "orm['base.DimensionDefinition']"}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': "orm['base.DimensionDevice']"}),
            'event_utc_date': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.DimensionUTCDate']", 'null': 'True'}),
            'event_utc_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': "orm['base.DimensionItem']"}),
            'last_modified_utc': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'mcc': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'mnc': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'platform': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': "orm['base.DimensionPlatform']"}),
            'price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': "orm['base.DimensionProduct']"}),
            'retail_model': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': "orm['base.DimensionRetailModel']"}),
            'right': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': "orm['base.DimensionRight']"}),
            'territory': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': "orm['base.DimensionTerritory']"}),
            'transaction_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'transaction_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.DimensionStoreTransactionStatus']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': "orm['base.DimensionUser']"}),
            'window': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': "orm['base.DimensionWindow']"})
        },
        'base.service': {
            'Meta': {'object_name': 'Service', 'db_table': "'service'"},
            'access_key': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '32'}),
            'access_secret': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '32'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        }
    }

    complete_apps = ['base']