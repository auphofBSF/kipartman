# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-17 23:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20170516_0939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='part',
            name='comment',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]