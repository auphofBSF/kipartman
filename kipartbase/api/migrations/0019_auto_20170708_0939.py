# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-08 09:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_partdistributor_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='partcategory',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='part',
            name='comment',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='part',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
    ]
