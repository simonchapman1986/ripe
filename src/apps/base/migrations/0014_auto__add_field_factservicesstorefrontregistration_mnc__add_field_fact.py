# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'FactServicesStorefrontRegistration.mnc'
        db.add_column('fact_services_storefront_registrations', 'mnc',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True),
                      keep_default=False)

        # Adding field 'FactServicesStorefrontRegistration.mcc'
        db.add_column('fact_services_storefront_registrations', 'mcc',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True),
                      keep_default=False)


        # Changing field 'DimensionRetailModel.model'
        db.alter_column('dim_retail_model', 'model', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))
        # Deleting field 'DimensionDevice.device_mnc'
        db.delete_column('dim_device', 'device_mnc')

        # Deleting field 'DimensionDevice.device_mcc'
        db.delete_column('dim_device', 'device_mcc')


    def backwards(self, orm):
        # Deleting field 'FactServicesStorefrontRegistration.mnc'
        db.delete_column('fact_services_storefront_registrations', 'mnc')

        # Deleting field 'FactServicesStorefrontRegistration.mcc'
        db.delete_column('fact_services_storefront_registrations', 'mcc')


        # Changing field 'DimensionRetailModel.model'
        db.alter_column('dim_retail_model', 'model', self.gf('django.db.models.fields.CharField')(default='', max_length=255))
        # Adding field 'DimensionDevice.device_mnc'
        db.add_column('dim_device', 'device_mnc',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=3, null=True, blank=True),
                      keep_default=False)

        # Adding field 'DimensionDevice.device_mcc'
        db.add_column('dim_device', 'device_mcc',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=3, null=True, blank=True),
                      keep_default=False)


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
            'account_created': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'account_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
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
            'definition': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'base.dimensiondevice': {
            'Meta': {'unique_together': "(('os', 'make', 'model', 'os_version'),)", 'object_name': 'DimensionDevice', 'db_table': "'dim_device'"},
            'device_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '36', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'make': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'os': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'os_version': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'})
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
            'provider_id': ('django.db.models.fields.CharField', [], {'max_length': '128L', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
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
            'model': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
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
            'country_of_residence': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'external_user_id': ('django.db.models.fields.CharField', [], {'default': "'00000000-0000-0000-0000-000000000000'", 'max_length': '36', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_user_id': ('django.db.models.fields.CharField', [], {'default': "'00000000-0000-0000-0000-000000000000'", 'max_length': '36', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'marketing_preference': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
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
            'definition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.DimensionDefinition']", 'null': 'True', 'blank': 'True'}),
            'delivery_date': ('django.db.models.fields.DateTimeField', [], {'default': 'None'}),
            'duration': ('django.db.models.fields.IntegerField', [], {'default': "''", 'max_length': '10'}),
            'event_date': ('django.db.models.fields.DateField', [], {'default': 'None'}),
            'event_utc_date': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.DimensionUTCDate']"}),
            'event_utc_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'None'}),
            'file_size': ('django.db.models.fields.BigIntegerField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'matched_item'", 'to': "orm['base.DimensionItem']"}),
            'languages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['base.DimensionLanguage']", 'symmetrical': 'False'}),
            'last_modified_utc': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'processing_state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.DimensionProcessingState']"}),
            'provider': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'matched_provider'", 'to': "orm['base.DimensionItemProvider']"}),
            'spec_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'territory': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.DimensionTerritory']"}),
            'used_asset_ids': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['base.DimensionAssets']", 'symmetrical': 'False'})
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
        'base.factserviceslicensingdelivery': {
            'Meta': {'object_name': 'FactServicesLicensingDelivery', 'db_table': "'fact_services_licensing_delivery'"},
            'device': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': "orm['base.DimensionDevice']"}),
            'drm_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'event_utc_date': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.DimensionUTCDate']", 'null': 'True'}),
            'event_utc_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'transaction_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': "orm['base.DimensionUser']"})
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
            'account': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': "orm['base.DimensionAccount']"}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.DimensionClient']"}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'default': '-1', 'to': "orm['base.DimensionDevice']"}),
            'event_utc_date': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.DimensionUTCDate']"}),
            'event_utc_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified_utc': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'mcc': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'mnc': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
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
            'last_4_digits': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '4', 'null': 'True'}),
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