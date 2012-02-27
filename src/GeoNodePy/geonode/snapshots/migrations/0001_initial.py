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
            ('unitid', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('short_desc', self.gf('markupfield.fields.MarkupField')(null=True, rendered_field=True, blank=True)),
            ('short_desc_markup_type', self.gf('django.db.models.fields.CharField')(default='markdown', max_length=30, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('_short_desc_rendered', self.gf('django.db.models.fields.TextField')()),
            ('regiontype', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['snapshots.Regiontype'], null=True, blank=True)),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')()),
        ))
        db.send_create_signal('snapshots', ['Regionalunit'])

        # Adding model 'Visualization'
        db.create_table('snapshots_visualization', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('regiontype', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['snapshots.Regiontype'])),
            ('sessionstate', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('year', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('overviewmap', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('snapshots', ['Visualization'])

        # Adding M2M table for field topics on 'Visualization'
        db.create_table('snapshots_visualization_topics', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('visualization', models.ForeignKey(orm['snapshots.visualization'], null=False)),
            ('topic', models.ForeignKey(orm['mbdc.topic'], null=False))
        ))
        db.create_unique('snapshots_visualization_topics', ['visualization_id', 'topic_id'])

        # Adding M2M table for field source on 'Visualization'
        db.create_table('snapshots_visualization_source', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('visualization', models.ForeignKey(orm['snapshots.visualization'], null=False)),
            ('datasource', models.ForeignKey(orm['mbdc.datasource'], null=False))
        ))
        db.create_unique('snapshots_visualization_source', ['visualization_id', 'datasource_id'])


    def backwards(self, orm):
        
        # Deleting model 'Regiontype'
        db.delete_table('snapshots_regiontype')

        # Deleting model 'Regionalunit'
        db.delete_table('snapshots_regionalunit')

        # Deleting model 'Visualization'
        db.delete_table('snapshots_visualization')

        # Removing M2M table for field topics on 'Visualization'
        db.delete_table('snapshots_visualization_topics')

        # Removing M2M table for field source on 'Visualization'
        db.delete_table('snapshots_visualization_source')


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