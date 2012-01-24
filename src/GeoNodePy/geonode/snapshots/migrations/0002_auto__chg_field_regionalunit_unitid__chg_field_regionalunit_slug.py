# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Regionalunit.unitid'
        db.alter_column('snapshots_regionalunit', 'unitid', self.gf('django.db.models.fields.CharField')(max_length=20))

        # Changing field 'Regionalunit.slug'
        db.alter_column('snapshots_regionalunit', 'slug', self.gf('django.db.models.fields.SlugField')(default='slug', max_length=50))


    def backwards(self, orm):
        
        # Changing field 'Regionalunit.unitid'
        db.alter_column('snapshots_regionalunit', 'unitid', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'Regionalunit.slug'
        db.alter_column('snapshots_regionalunit', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=50, null=True))


    models = {
        'snapshots.regionalunit': {
            'Meta': {'ordering': "['name']", 'object_name': 'Regionalunit'},
            'geometry': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'regiontype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['snapshots.Regiontype']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'unitid': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'snapshots.regiontype': {
            'Meta': {'object_name': 'Regiontype'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        }
    }

    complete_apps = ['snapshots']
