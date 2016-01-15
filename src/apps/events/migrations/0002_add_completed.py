# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.add_column('event_log', 'completed',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Flags'
        db.delete_column('event_log', 'completed')

    models = {
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
        'events.event_log': {
            'Meta': {'object_name': 'Log', 'db_table': "'event_log'"},
            'packet': ('django.db.models.fields.TextField', [], {}),
            'event': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'event_utc_date': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.DimensionUTCDate']"}),
            'event_utc_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
        }
    }

    complete_apps = ['events']