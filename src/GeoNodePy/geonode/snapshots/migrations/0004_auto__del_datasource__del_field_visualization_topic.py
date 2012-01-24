# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'Datasource'
        db.delete_table('snapshots_datasource')

        # Deleting field 'Visualization.topic'
        db.delete_column('snapshots_visualization', 'topic')

        # Adding M2M table for field topic on 'Visualization'
        db.create_table('snapshots_visualization_topic', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('visualization', models.ForeignKey(orm['snapshots.visualization'], null=False)),
            ('topic', models.ForeignKey(orm['mbdc.topic'], null=False))
        ))
        db.create_unique('snapshots_visualization_topic', ['visualization_id', 'topic_id'])


    def backwards(self, orm):
        
        # Adding model 'Datasource'
        db.create_table('snapshots_datasource', (
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
        ))
        db.send_create_signal('snapshots', ['Datasource'])

        # Adding field 'Visualization.topic'
        db.add_column('snapshots_visualization', 'topic', self.gf('django.db.models.fields.CharField')(default=0, max_length=20), keep_default=False)

        # Removing M2M table for field topic on 'Visualization'
        db.delete_table('snapshots_visualization_topic')


    models = {
        'mbdc.datasource': {
            'Meta': {'object_name': 'Datasource'},
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
        },
        'snapshots.visualization': {
            'Meta': {'object_name': 'Visualization'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'regiontype': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['snapshots.Regiontype']"}),
            'sessionstate': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'source': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['mbdc.Datasource']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'topic': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['mbdc.Topic']", 'symmetrical': 'False'}),
            'year': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['snapshots']
