# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class PartCategory(MPTTModel):
    parent = TreeForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True, db_index=True)
    name = models.TextField()
    description = models.TextField(blank=True, default='')
    class MPTTMeta:
        order_insertion_by = ['name']
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)


class Part(models.Model):
    name = models.TextField()
    description = models.TextField(blank=True, default='')
    comment = models.TextField(blank=True, default='')
    category = models.ForeignKey('PartCategory', on_delete=models.DO_NOTHING, null=True, blank=True, default=None)
    footprint = models.ForeignKey('Footprint', on_delete=models.DO_NOTHING, null=True, blank=True, default=None)
    model = models.ForeignKey('Model', on_delete=models.DO_NOTHING, null=True, blank=True, default=None)
    childs = models.ManyToManyField('Part', blank=True)
    #parameters is defined inside PartParameter by ForeignKey part
    #offers is defined inside PartOffer by ForeignKey part
    #manufacturers is defined inside PartManufacturer by ForeignKey part
    #storages is defined inside PartStorage by ForeignKey part
    #attachements: TODO
    # octopart fields
    octopart = models.TextField(null=True, blank=True, default=None)
    updated = models.DateTimeField(null=True, blank=True, default=None)
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)

class PartParameter(models.Model):
    part = models.ForeignKey('Part', related_name='parameters', null=False, blank=False, default=None)
    name = models.TextField()
    description = models.TextField(blank=True)
    unit = models.ForeignKey('Unit', on_delete=models.DO_NOTHING, null=True, default=None, blank=True)
    numeric = models.BooleanField()
    text_value = models.TextField(null=True, blank=True)
    min_value = models.FloatField(null=True)
    min_prefix = models.ForeignKey('UnitPrefix', related_name='min', on_delete=models.DO_NOTHING, null=True, default=None, blank=True)
    nom_value = models.FloatField(null=True)
    nom_prefix = models.ForeignKey('UnitPrefix', related_name='nom', on_delete=models.DO_NOTHING, null=True, default=None, blank=True)
    max_value = models.FloatField(null=True)
    max_prefix = models.ForeignKey('UnitPrefix', related_name='max', on_delete=models.DO_NOTHING, null=True, default=None, blank=True)
    def __unicode__(self):
        if self.id:
            return '%d: %s' % (self.id, self.name)
        else:
            return '<None>: %s' % (self.name)
            


class PartManufacturer(models.Model):
    part = models.ForeignKey('Part', related_name='manufacturers', null=False, blank=False, default=None)
    manufacturer = models.ForeignKey('Manufacturer', on_delete=models.DO_NOTHING, null=False)
    part_name = models.TextField()
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)


class PartOffer(models.Model):
    part = models.ForeignKey('Part', related_name='offers', null=False, blank=False, default=None)
    distributor = models.ForeignKey('Distributor', on_delete=models.DO_NOTHING, null=True, blank=True, default=None)
    packaging_unit = models.IntegerField()
    quantity = models.IntegerField()
    unit_price = models.FloatField()
    currency = models.TextField(blank=True)
    sku = models.TextField(blank=True)
    updated = models.DateTimeField()
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)
    

class PartStorage(models.Model):
    part = models.ForeignKey('Part', related_name='storages', null=False, blank=False, default=None)
    storage = models.ForeignKey('Storage', on_delete=models.DO_NOTHING, null=True, blank=True, default=None)
    quantity = models.IntegerField()
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)

class Manufacturer(models.Model):
    name = models.TextField(blank=False)
    address = models.TextField(null=True, blank=True, default='')
    website = models.TextField(null=True, blank=True, default='')
    email = models.TextField(null=True, blank=True, default='')
    phone = models.TextField(null=True, blank=True, default='')
    comment = models.TextField(null=True, blank=True, default='')
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)


class Distributor(models.Model):
    name = models.TextField(blank=False)
    address = models.TextField(null=True, blank=True, default='')
    website = models.TextField(null=True, blank=True, default='')
    sku_url = models.TextField(null=True, blank=True, default='')
    email = models.TextField(null=True, blank=True, default='')
    phone = models.TextField(null=True, blank=True, default='')
    comment = models.TextField(null=True, blank=True, default='')
    allowed = models.BooleanField(null=False, default=True)
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)

class FootprintCategory(MPTTModel):
    parent = TreeForeignKey('FootprintCategory', on_delete=models.DO_NOTHING, null=True, default=None, blank=True)
    name = models.TextField()
    description = models.TextField(blank=True, default='')
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)


class Footprint(models.Model):
    category = models.ForeignKey('FootprintCategory', on_delete=models.DO_NOTHING, null=True, default=None, blank=True)
    name = models.TextField()
    description = models.TextField(blank=True, default='')
    comment = models.TextField(blank=True, default='')
    image = models.ForeignKey('File', related_name='image', on_delete=models.DO_NOTHING, null=True, default=None)
    footprint = models.ForeignKey('File', related_name='footprint', on_delete=models.DO_NOTHING, null=True, default=None)
    snapeda = models.TextField(null=True, blank=True)
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)
    
class ModelCategory(MPTTModel):
    parent = TreeForeignKey('ModelCategory', on_delete=models.DO_NOTHING, null=True, default=None, blank=True)
    name = models.TextField()
    description = models.TextField(blank=True, default='')
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)


class Model(models.Model):
    category = models.ForeignKey('ModelCategory', on_delete=models.DO_NOTHING, null=True, default=None, blank=True)
    name = models.TextField()
    description = models.TextField(blank=True, default='')
    comment = models.TextField(blank=True, default='')
    image = models.ForeignKey('File', related_name='model_image', on_delete=models.DO_NOTHING, null=True, default=None)
    model = models.ForeignKey('File', related_name='model_file', on_delete=models.DO_NOTHING, null=True, default=None)
    snapeda = models.TextField(null=True, blank=True)
    childs = models.ManyToManyField('Model', related_name='model_childs', blank=True)
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)

class File(models.Model):
    source_name = models.TextField()
    storage_path = models.TextField()
    def __unicode__(self):
        return '%d: %s, %s' % (self.id, self.source_name, self.storage_path)


class Unit(models.Model):
    name = models.TextField()
    symbol = models.TextField(default='')
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)


class UnitPrefix(models.Model):
    name = models.TextField()
    # suffix name
    symbol = models.TextField()
    # value contains the exponent part
    power = models.TextField()
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)

class StorageCategory(MPTTModel):
    parent = TreeForeignKey('StorageCategory', on_delete=models.DO_NOTHING, null=True, default=None, blank=True)
    name = models.TextField()
    description = models.TextField(blank=True, default='')
    def __unicode__(self):
        return '%d: %s' % (self.id, self.name)

class Storage(models.Model):
    category = models.ForeignKey('StorageCategory', on_delete=models.DO_NOTHING, null=True, default=None, blank=True)
    name = models.TextField()
    description = models.TextField(blank=True, default='')
    comment = models.TextField(blank=True, default='')

class PartStorageHistory(models.Model):
    part = models.ForeignKey('Part', null=False, blank=False, default=None)
    location = models.ForeignKey('Storage', null=False, blank=False, default=None)
    reason = models.TextField(blank=False)
    amount = models.IntegerField()
