# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-06-25 11:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0002_auto_20200621_2207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.Category', verbose_name='\u7c7b\u522b'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='gdesc',
            field=models.CharField(max_length=100, verbose_name='\u5546\u54c1\u63cf\u8ff0'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='gname',
            field=models.CharField(max_length=100, verbose_name='\u5546\u54c1\u540d\u79f0'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='oldprice',
            field=models.DecimalField(decimal_places=2, max_digits=5, verbose_name='\u65e7\u4ef7\u683c'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=5, verbose_name='\u65b0\u4ef7\u683c'),
        ),
    ]
