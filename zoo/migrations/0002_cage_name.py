# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-12 18:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zoo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cage',
            name='name',
            field=models.CharField(max_length=20, null=True),
        ),
    ]