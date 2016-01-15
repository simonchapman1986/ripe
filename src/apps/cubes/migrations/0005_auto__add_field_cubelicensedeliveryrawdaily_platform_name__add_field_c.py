# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'CubeLicenseDeliveryRawDaily.platform_name'
        db.add_column('summary_license_delivery_raw_daily', 'platform_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255),
                      keep_default=False)

        # Adding field 'CubeLicenseDeliveryRawDaily.item_id'
        db.add_column('summary_license_delivery_raw_daily', 'item_id',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=36, blank=True),
                      keep_default=False)

        # Adding field 'CubeLicenseDeliveryRawDaily.item_title'
        db.add_column('summary_license_delivery_raw_daily', 'item_title',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'CubeLicenseDeliveryRawDaily.platform_name'
        db.delete_column('summary_license_delivery_raw_daily', 'platform_name')

        # Deleting field 'CubeLicenseDeliveryRawDaily.item_id'
        db.delete_column('summary_license_delivery_raw_daily', 'item_id')

        # Deleting field 'CubeLicenseDeliveryRawDaily.item_title'
        db.delete_column('summary_license_delivery_raw_daily', 'item_title')


    models = {
        'cubes.cubecontent': {
            'Meta': {'object_name': 'CubeContent', 'db_table': "'summary_content_daily'"},
            'added_to_client': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'asset_role_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'client_id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'content_provider': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 19, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
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
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 19, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
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
        'cubes.cubelicensedeliveryrawdaily': {
            'Meta': {'object_name': 'CubeLicenseDeliveryRawDaily', 'db_table': "'summary_license_delivery_raw_daily'"},
            'client_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '36'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 19, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'day': ('django.db.models.fields.SmallIntegerField', [], {}),
            'day_name': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'day_of_week': ('django.db.models.fields.IntegerField', [], {}),
            'device_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '36', 'blank': 'True'}),
            'device_os': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'device_os_version': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'drm_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'external_user_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'internal_user_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'item_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'item_title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'make': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'month': ('django.db.models.fields.SmallIntegerField', [], {}),
            'platform_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'quarter': ('django.db.models.fields.SmallIntegerField', [], {}),
            'territory_code': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10'}),
            'transaction_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'week_of_year': ('django.db.models.fields.SmallIntegerField', [], {}),
            'year': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        'cubes.cubeplaysbyitem': {
            'Meta': {'object_name': 'CubePlaysByItem', 'db_table': "'summary_plays_by_item_daily'"},
            'client_id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 19, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
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
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 19, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
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
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 19, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
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
        'cubes.cubesubscriptionrevenuedaily': {
            'Meta': {'object_name': 'CubeSubscriptionRevenueDaily', 'db_table': "'summary_subscription_revenue_daily'"},
            'card_suffix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'client_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '36'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 19, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'day': ('django.db.models.fields.SmallIntegerField', [], {}),
            'day_name': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'day_of_week': ('django.db.models.fields.IntegerField', [], {}),
            'first_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'month': ('django.db.models.fields.SmallIntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'os': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2'}),
            'quarter': ('django.db.models.fields.SmallIntegerField', [], {}),
            'subscription_status': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'territory_code': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'week_of_year': ('django.db.models.fields.SmallIntegerField', [], {}),
            'year': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        'cubes.cubesubscriptionsdaily': {
            'Meta': {'object_name': 'CubeSubscriptionsDaily', 'db_table': "'summary_subscriptions_daily'"},
            'average_per_day': ('django.db.models.fields.IntegerField', [], {}),
            'breakdown_pct': ('django.db.models.fields.IntegerField', [], {}),
            'change': ('django.db.models.fields.IntegerField', [], {}),
            'client_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '36'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 19, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
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