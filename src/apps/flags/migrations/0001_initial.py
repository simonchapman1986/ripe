# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Flags'
        db.create_table('flags', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('event', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('event_utc_date', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.DimensionUTCDate'])),
            ('event_utc_datetime', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('flags', ['Flags'])


    def backwards(self, orm):
        # Deleting model 'Flags'
        db.delete_table('flags')


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
        'flags.flags': {
            'Meta': {'object_name': 'Flags', 'db_table': "'flags'"},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'event': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'event_utc_date': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.DimensionUTCDate']"}),
            'event_utc_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['flags']