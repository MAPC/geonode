# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Datasource'
        db.create_table('snapshots_datasource', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('snapshots', ['Datasource'])

        # Adding model 'Visualization'
        db.create_table('snapshots_visualization', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('topic', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('regiontype', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['snapshots.Regiontype'])),
            ('sessionstate', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('year', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
        ))
        db.send_create_signal('snapshots', ['Visualization'])

        # Adding M2M table for field source on 'Visualization'
        db.create_table('snapshots_visualization_source', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('visualization', models.ForeignKey(orm['snapshots.visualization'], null=False)),
            ('datasource', models.ForeignKey(orm['snapshots.datasource'], null=False))
        ))
        db.create_unique('snapshots_visualization_source', ['visualization_id', 'datasource_id'])


    def backwards(self, orm):
        
        # Deleting model 'Datasource'
        db.delete_table('snapshots_datasource')

        # Deleting model 'Visualization'
        db.delete_table('snapshots_visualization')

        # Removing M2M table for field source on 'Visualization'
        db.delete_table('snapshots_visualization_source')


    models = {
        'snapshots.datasource': {
            'Meta': {'object_name': 'Datasource'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
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
            'source': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['snapshots.Datasource']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'topic': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'year': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['snapshots']
