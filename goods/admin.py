# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from goods.models import Goods


@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    list_display = ('gname', 'gdesc', 'oldprice', 'price', 'category')
    search_fields = ['gname', 'gdesc', 'category']
