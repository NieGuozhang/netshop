# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-06-23 15:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='uname',
            field=models.EmailField(max_length=100, unique=True),
        ),
    ]