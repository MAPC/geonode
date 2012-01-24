# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Regiontype'
        db.create_table('snapshots_regiontype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
        ))
        db.send_create_signal('snapshots', ['Regiontype'])

        # Adding model 'Regionalunit'
        db.create_table('snapshots_regionalunit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('unitid', self.gf('django.db.models.fields.IntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(db_index=True, max_length=50, null=True, blank=True)),
            ('regiontype', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['snapshots.Regiontype'], null=True, blank=True)),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')()),
        ))
        db.send_create_signal('snapshots', ['Regionalunit'])


    def backwards(self, orm):
        
        # Deleting model 'Regiontype'
        db.delete_table('snapshots_regiontype')

        # Deleting model 'Regionalunit'
        db.delete_table('snapshots_regionalunit')


    models = {
        'snapshots.regionalunit': {
            'Meta': {'object_name': 'Regionalunit'},
            'geometry': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'regiontype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['snapshots.Regiontype']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'unitid': ('django.db.models.fields.IntegerField', [], {})
        },
        'snapshots.regiontype': {
            'Meta': {'object_name': 'Regiontype'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        }
    }

    complete_apps = ['snapshots']
