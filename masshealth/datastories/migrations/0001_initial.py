# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Page'
        db.create_table('masshealth_datastories_page', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(default='', max_length=255, blank=True)),
            ('visualization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['visualizations.Visualization'], null=True, blank=True)),
        ))
        db.send_create_signal('datastories', ['Page'])

        # Adding model 'Story'
        db.create_table('masshealth_datastories_story', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100, db_index=True)),
            ('abstract', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(default='', max_length=255, blank=True)),
        ))
        db.send_create_signal('datastories', ['Story'])

        # Adding M2M table for field places on 'Story'
        db.create_table('masshealth_datastories_story_places', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('story', models.ForeignKey(orm['datastories.story'], null=False)),
            ('place', models.ForeignKey(orm['places.place'], null=False))
        ))
        db.create_unique('masshealth_datastories_story_places', ['story_id', 'place_id'])

        # Adding model 'StoryPage'
        db.create_table('masshealth_datastories_storypage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('story', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datastories.Story'])),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datastories.Page'])),
            ('page_number', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('datastories', ['StoryPage'])


    def backwards(self, orm):
        
        # Deleting model 'Page'
        db.delete_table('masshealth_datastories_page')

        # Deleting model 'Story'
        db.delete_table('masshealth_datastories_story')

        # Removing M2M table for field places on 'Story'
        db.delete_table('masshealth_datastories_story_places')

        # Deleting model 'StoryPage'
        db.delete_table('masshealth_datastories_storypage')


    models = {
        'datastories.page': {
            'Meta': {'object_name': 'Page', 'db_table': "'masshealth_datastories_page'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'visualization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['visualizations.Visualization']", 'null': 'True', 'blank': 'True'})
        },
        'datastories.story': {
            'Meta': {'object_name': 'Story', 'db_table': "'masshealth_datastories_story'"},
            'abstract': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'pages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['datastories.Page']", 'through': "orm['datastories.StoryPage']", 'symmetrical': 'False'}),
            'places': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'datastories'", 'blank': 'True', 'to': "orm['places.Place']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'datastories.storypage': {
            'Meta': {'object_name': 'StoryPage', 'db_table': "'masshealth_datastories_storypage'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datastories.Page']"}),
            'page_number': ('django.db.models.fields.IntegerField', [], {}),
            'story': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datastories.Story']"})
        },
        'places.place': {
            'Meta': {'ordering': "['name']", 'object_name': 'Place', 'db_table': "'masshealth_places_place'"},
            'geometry': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'srid': '26986', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'profile': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'program_desc': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'regiontype': ('django.db.models.fields.CharField', [], {'default': "'Cities and Towns'", 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'unitid': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'visualizations.visualization': {
            'Meta': {'object_name': 'Visualization', 'db_table': "'masshealth_visualizations_visualization'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'template': ('django.db.models.fields.files.FileField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['datastories']
