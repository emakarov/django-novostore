# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'WebsiteMenuItem'
        db.create_table(u'sitemanagement_websitemenuitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['sitemanagement.WebsiteMenuItem'])),
            ('websitemenu', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sitemanagement.WebsiteMenu'])),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=80, db_index=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal(u'sitemanagement', ['WebsiteMenuItem'])


    def backwards(self, orm):
        # Deleting model 'WebsiteMenuItem'
        db.delete_table(u'sitemanagement_websitemenuitem')


    models = {
        u'sitemanagement.websitemenu': {
            'Meta': {'object_name': 'WebsiteMenu'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'db_index': 'True'})
        },
        u'sitemanagement.websitemenublock': {
            'Meta': {'object_name': 'WebsiteMenuBlock'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '80', 'db_index': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'websitemenu': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sitemanagement.WebsiteMenu']"})
        },
        u'sitemanagement.websitemenublockitem': {
            'Meta': {'object_name': 'WebsiteMenuBlockItem'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '80', 'db_index': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'websitemenublock': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': u"orm['sitemanagement.WebsiteMenuBlock']"})
        },
        u'sitemanagement.websitemenuitem': {
            'Meta': {'object_name': 'WebsiteMenuItem'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['sitemanagement.WebsiteMenuItem']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '80', 'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'websitemenu': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sitemanagement.WebsiteMenu']"})
        }
    }

    complete_apps = ['sitemanagement']