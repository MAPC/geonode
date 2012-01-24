# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Visualization.overviewmap'
        db.add_column('snapshots_visualization', 'overviewmap', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Visualization.overviewmap'
        db.delete_column('snapshots_visualization', 'overviewmap')


    models = {
        'mbdc.datasource': {
            'Meta': {'ordering': "['title']", 'object_name': 'Datasource'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'mbdc.topic': {
            'Meta': {'ordering': "['order']", 'object_name': 'Topic'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'snapshots.regionalunit': {
            'Meta': {'ordering': "['name']", 'object_name': 'Regionalunit'},
            '_short_desc_rendered': ('django.db.models.fields.TextField', [], {}),
            'geometry': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'regiontype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['snapshots.Regiontype']", 'null': 'True', 'blank': 'True'}),
            'short_desc': ('markupfield.fields.MarkupField', [], {'null': 'True', 'rendered_field': 'True', 'blank': 'True'}),
            'short_desc_markup_type': ('django.db.models.fields.CharField', [], {'default': "'markdown'", 'max_length': '30', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'unitid': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'snapshots.regiontype': {
            'Meta': {'object_name': 'Regiontype'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'snapshots.visualization': {
            'Meta': {'ordering': "['title']", 'object_name': 'Visualization'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'overviewmap': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'regiontype': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['snapshots.Regiontype']"}),
            'sessionstate': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'source': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['mbdc.Datasource']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'topics': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'snapshot_visualization'", 'symmetrical': 'False', 'to': "orm['mbdc.Topic']"}),
            'year': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['snapshots']
