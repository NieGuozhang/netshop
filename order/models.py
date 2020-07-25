# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from goods.models import Goods, Color, Size
from userapp.models import Address, UserInfo


class Order(models.Model):
    out_trade_num = models.UUIDField(verbose_name='唯一的编码')
    order_num = models.CharField(max_length=50)
    trade_no = models.CharField(max_length=120, default='')
    status = models.CharField(max_length=20, default='待支付')
    payway = models.CharField(max_length=20, default='alipay')
    address = models.ForeignKey(Address)
    user = models.ForeignKey(UserInfo)

    class Meta:
        verbose_name = '订单表'


class OrderItem(models.Model):
    goodsid = models.PositiveIntegerField()
    colorid = models.PositiveIntegerField()
    sizeid = models.PositiveIntegerField()
    count = models.PositiveIntegerField()
    order = models.ForeignKey(Order)

    class Meta:
        verbose_name = '订单项表'
