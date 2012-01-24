# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Hero.order'
        db.add_column('mbdc_hero', 'order', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)

        # Adding field 'Hero.active'
        db.add_column('mbdc_hero', 'active', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Changing field 'Hero.navtitle'
        db.alter_column('mbdc_hero', 'navtitle', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'Hero.navsubtitle'
        db.alter_column('mbdc_hero', 'navsubtitle', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))


    def backwards(self, orm):
        
        # Deleting field 'Hero.order'
        db.delete_column('mbdc_hero', 'order')

        # Deleting field 'Hero.active'
        db.delete_column('mbdc_hero', 'active')

        # User chose to not deal with backwards NULL issues for 'Hero.navtitle'
        raise RuntimeError("Cannot reverse this migration. 'Hero.navtitle' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Hero.navsubtitle'
        raise RuntimeError("Cannot reverse this migration. 'Hero.navsubtitle' and its values cannot be restored.")


    models = {
        'mbdc.hero': {
            'Meta': {'object_name': 'Hero'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'navsubtitle': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'navtitle': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['mbdc']
