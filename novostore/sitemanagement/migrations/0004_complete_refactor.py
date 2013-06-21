# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'WebsiteMenuItem'
        db.delete_table(u'sitemanagement_websitemenuitem')

        # Deleting model 'WebsiteMenuBlock'
        db.delete_table(u'sitemanagement_websitemenublock')

        # Deleting model 'WebsiteMenuBlockItem'
        db.delete_table(u'sitemanagement_websitemenublockitem')

        # Deleting field 'WebsiteMenu.name'
        db.delete_column(u'sitemanagement_websitemenu', 'name')

        # Adding field 'WebsiteMenu.parent'
        db.add_column(u'sitemanagement_websitemenu', 'parent',
                      self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['sitemanagement.WebsiteMenu']),
                      keep_default=False)

        # Adding field 'WebsiteMenu.text'
        db.add_column(u'sitemanagement_websitemenu', 'text',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=80, db_index=True),
                      keep_default=False)

        # Adding field 'WebsiteMenu.url'
        db.add_column(u'sitemanagement_websitemenu', 'url',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'WebsiteMenu.order'
        db.add_column(u'sitemanagement_websitemenu', 'order',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=1),
                      keep_default=False)

        # Adding field 'WebsiteMenu.lft'
        db.add_column(u'sitemanagement_websitemenu', 'lft',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=1, db_index=True),
                      keep_default=False)

        # Adding field 'WebsiteMenu.rght'
        db.add_column(u'sitemanagement_websitemenu', 'rght',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=1, db_index=True),
                      keep_default=False)

        # Adding field 'WebsiteMenu.tree_id'
        db.add_column(u'sitemanagement_websitemenu', 'tree_id',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=1, db_index=True),
                      keep_default=False)

        # Adding field 'WebsiteMenu.level'
        db.add_column(u'sitemanagement_websitemenu', 'level',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=1, db_index=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'WebsiteMenuItem'
        db.create_table(u'sitemanagement_websitemenuitem', (
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(related_name='children', null=True, to=orm['sitemanagement.WebsiteMenuItem'], blank=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=80, db_index=True)),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('websitemenu', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sitemanagement.WebsiteMenu'], null=True, blank=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'sitemanagement', ['WebsiteMenuItem'])

        # Adding model 'WebsiteMenuBlock'
        db.create_table(u'sitemanagement_websitemenublock', (
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=80, db_index=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('websitemenu', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sitemanagement.WebsiteMenu'])),
        ))
        db.send_create_signal(u'sitemanagement', ['WebsiteMenuBlock'])

        # Adding model 'WebsiteMenuBlockItem'
        db.create_table(u'sitemanagement_websitemenublockitem', (
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=80, db_index=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('websitemenublock', self.gf('django.db.models.fields.related.ForeignKey')(related_name='items', to=orm['sitemanagement.WebsiteMenuBlock'])),
        ))
        db.send_create_signal(u'sitemanagement', ['WebsiteMenuBlockItem'])


        # User chose to not deal with backwards NULL issues for 'WebsiteMenu.name'
        raise RuntimeError("Cannot reverse this migration. 'WebsiteMenu.name' and its values cannot be restored.")
        # Deleting field 'WebsiteMenu.parent'
        db.delete_column(u'sitemanagement_websitemenu', 'parent_id')

        # Deleting field 'WebsiteMenu.text'
        db.delete_column(u'sitemanagement_websitemenu', 'text')

        # Deleting field 'WebsiteMenu.url'
        db.delete_column(u'sitemanagement_websitemenu', 'url')

        # Deleting field 'WebsiteMenu.order'
        db.delete_column(u'sitemanagement_websitemenu', 'order')

        # Deleting field 'WebsiteMenu.lft'
        db.delete_column(u'sitemanagement_websitemenu', 'lft')

        # Deleting field 'WebsiteMenu.rght'
        db.delete_column(u'sitemanagement_websitemenu', 'rght')

        # Deleting field 'WebsiteMenu.tree_id'
        db.delete_column(u'sitemanagement_websitemenu', 'tree_id')

        # Deleting field 'WebsiteMenu.level'
        db.delete_column(u'sitemanagement_websitemenu', 'level')


    models = {
        u'sitemanagement.websitemenu': {
            'Meta': {'object_name': 'WebsiteMenu'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['sitemanagement.WebsiteMenu']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '80', 'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['sitemanagement']