# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-05 00:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20170602_1454'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partdistributor',
            name='package_price',
        ),
    ]
