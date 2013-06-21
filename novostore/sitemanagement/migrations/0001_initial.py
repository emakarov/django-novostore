# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'WebsiteMenu'
        db.create_table('sitemanagement_websitemenu', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80, db_index=True)),
        ))
        db.send_create_signal('sitemanagement', ['WebsiteMenu'])

        # Adding model 'WebsiteMenuBlock'
        db.create_table('sitemanagement_websitemenublock', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('websitemenu', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sitemanagement.WebsiteMenu'])),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=80, db_index=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('sitemanagement', ['WebsiteMenuBlock'])

        # Adding model 'WebsiteMenuBlockItem'
        db.create_table('sitemanagement_websitemenublockitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('websitemenublock', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sitemanagement.WebsiteMenuBlock'])),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=80, db_index=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('sitemanagement', ['WebsiteMenuBlockItem'])


    def backwards(self, orm):
        
        # Deleting model 'WebsiteMenu'
        db.delete_table('sitemanagement_websitemenu')

        # Deleting model 'WebsiteMenuBlock'
        db.delete_table('sitemanagement_websitemenublock')

        # Deleting model 'WebsiteMenuBlockItem'
        db.delete_table('sitemanagement_websitemenublockitem')


    models = {
        'sitemanagement.websitemenu': {
            'Meta': {'object_name': 'WebsiteMenu'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'db_index': 'True'})
        },
        'sitemanagement.websitemenublock': {
            'Meta': {'object_name': 'WebsiteMenuBlock'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '80', 'db_index': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'websitemenu': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sitemanagement.WebsiteMenu']"})
        },
        'sitemanagement.websitemenublockitem': {
            'Meta': {'object_name': 'WebsiteMenuBlockItem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '80', 'db_index': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'websitemenublock': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sitemanagement.WebsiteMenuBlock']"})
        }
    }

    complete_apps = ['sitemanagement']
