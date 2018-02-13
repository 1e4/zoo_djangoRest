# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-12 19:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zoo', '0004_auto_20180212_2200'),
    ]

    operations = [
        migrations.AddField(
            model_name='animal',
            name='type',
            field=models.CharField(choices=[('Lion', 'lion'), ('Elephant', 'elephant'), ('Monkey', 'monkey'), ('Flamingo', 'flamingo'), ('Giraffe', 'giraffe')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='animal',
            name='name',
            field=models.CharField(max_length=30, null=True),
        ),
    ]