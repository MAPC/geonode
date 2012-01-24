# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Page'
        db.create_table('datastories_page', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('datastories', ['Page'])

        # Adding model 'Textpage'
        db.create_table('datastories_textpage', (
            ('page_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['datastories.Page'], unique=True, primary_key=True)),
            ('abstract', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('datastories', ['Textpage'])

        # Adding model 'Visualizationpage'
        db.create_table('datastories_visualizationpage', (
            ('page_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['datastories.Page'], unique=True, primary_key=True)),
            ('caption', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('visualization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['weave.Visualization'])),
        ))
        db.send_create_signal('datastories', ['Visualizationpage'])

        # Adding model 'Mappage'
        db.create_table('datastories_mappage', (
            ('page_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['datastories.Page'], unique=True, primary_key=True)),
            ('caption', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('map', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['maps.Map'])),
        ))
        db.send_create_signal('datastories', ['Mappage'])

        # Adding model 'Datastory'
        db.create_table('datastories_datastory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100, db_index=True)),
            ('abstract', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('datastories', ['Datastory'])

        # Adding unique constraint on 'Datastory', fields ['title', 'owner']
        db.create_unique('datastories_datastory', ['title', 'owner_id'])

        # Adding model 'Storypage'
        db.create_table('datastories_storypage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datastory', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datastories.Datastory'])),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datastories.Page'])),
            ('pageorder', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('datastories', ['Storypage'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Datastory', fields ['title', 'owner']
        db.delete_unique('datastories_datastory', ['title', 'owner_id'])

        # Deleting model 'Page'
        db.delete_table('datastories_page')

        # Deleting model 'Textpage'
        db.delete_table('datastories_textpage')

        # Deleting model 'Visualizationpage'
        db.delete_table('datastories_visualizationpage')

        # Deleting model 'Mappage'
        db.delete_table('datastories_mappage')

        # Deleting model 'Datastory'
        db.delete_table('datastories_datastory')

        # Deleting model 'Storypage'
        db.delete_table('datastories_storypage')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'datastories.datastory': {
            'Meta': {'unique_together': "(('title', 'owner'),)", 'object_name': 'Datastory'},
            'abstract': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'datastory': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['datastories.Page']", 'through': "orm['datastories.Storypage']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'datastories.mappage': {
            'Meta': {'object_name': 'Mappage', '_ormbases': ['datastories.Page']},
            'caption': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'map': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['maps.Map']"}),
            'page_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['datastories.Page']", 'unique': 'True', 'primary_key': 'True'})
        },
        'datastories.page': {
            'Meta': {'object_name': 'Page'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'datastories.storypage': {
            'Meta': {'object_name': 'Storypage'},
            'datastory': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datastories.Datastory']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datastories.Page']"}),
            'pageorder': ('django.db.models.fields.IntegerField', [], {})
        },
        'datastories.textpage': {
            'Meta': {'object_name': 'Textpage', '_ormbases': ['datastories.Page']},
            'abstract': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'page_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['datastories.Page']", 'unique': 'True', 'primary_key': 'True'})
        },
        'datastories.visualizationpage': {
            'Meta': {'object_name': 'Visualizationpage', '_ormbases': ['datastories.Page']},
            'caption': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'page_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['datastories.Page']", 'unique': 'True', 'primary_key': 'True'}),
            'visualization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['weave.Visualization']"})
        },
        'maps.map': {
            'Meta': {'object_name': 'Map'},
            'abstract': ('django.db.models.fields.TextField', [], {}),
            'center_x': ('django.db.models.fields.FloatField', [], {}),
            'center_y': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'projection': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'zoom': ('django.db.models.fields.IntegerField', [], {})
        },
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
        'weave.visualization': {
            'Meta': {'ordering': "['-last_modified']", 'object_name': 'Visualization'},
            'abstract': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'datasources': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'weave_datasources'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['mbdc.Datasource']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'original': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['weave.Visualization']", 'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'sessionstate': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'topics': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'weave_topics'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['mbdc.Topic']"}),
            'year': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['datastories']
