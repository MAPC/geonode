# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Hero'
        db.create_table('mbdc_hero', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('subtitle', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('navtitle', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('navsubtitle', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('mbdc', ['Hero'])


    def backwards(self, orm):
        
        # Deleting model 'Hero'
        db.delete_table('mbdc_hero')


    models = {
        'mbdc.hero': {
            'Meta': {'object_name': 'Hero'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'navsubtitle': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'navtitle': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['mbdc']
