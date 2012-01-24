# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Hero.navsubtitle'
        db.delete_column('mbdc_hero', 'navsubtitle')

        # Deleting field 'Hero.active'
        db.delete_column('mbdc_hero', 'active')

        # Deleting field 'Hero.navtitle'
        db.delete_column('mbdc_hero', 'navtitle')

        # Deleting field 'Hero.order'
        db.delete_column('mbdc_hero', 'order')


    def backwards(self, orm):
        
        # Adding field 'Hero.navsubtitle'
        db.add_column('mbdc_hero', 'navsubtitle', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True), keep_default=False)

        # Adding field 'Hero.active'
        db.add_column('mbdc_hero', 'active', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Hero.navtitle'
        db.add_column('mbdc_hero', 'navtitle', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True), keep_default=False)

        # Adding field 'Hero.order'
        db.add_column('mbdc_hero', 'order', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)


    models = {
        'mbdc.hero': {
            'Meta': {'object_name': 'Hero'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['mbdc']
