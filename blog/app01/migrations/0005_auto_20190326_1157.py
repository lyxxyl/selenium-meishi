# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-03-26 03:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0004_auto_20190326_1152'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='article_doen',
            new_name='article_down',
        ),
    ]