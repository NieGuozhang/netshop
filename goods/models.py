# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Category(models.Model):
    cname = models.CharField(max_length=10)

    def __str__(self):
        return self.cname


class Goods(models.Model):
    gname = models.CharField(max_length=100, verbose_name='商品名称')
    gdesc = models.CharField(max_length=100, verbose_name='商品描述')
    oldprice = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='旧价格')
    price = models.DecimalField(max_digits=5, decimal_places=2,verbose_name='新价格')
    category = models.ForeignKey(Category, verbose_name='类别')

    def __str__(self):
        return self.gname

    def getGImg(self):
        '''
        获取商品大图
        :return:
        '''
        return self.inventory_set.first().color.colorurl

    def getColors(self):
        '''
        获取商品所有颜色对象
        :return:
        '''
        colorList = []
        for inventory in self.inventory_set.all():
            color = inventory.color
            if color not in colorList:
                colorList.append(color)
        return colorList

    def getSizes(self):
        """
        获取商品所有大小
        :return:
        """
        sizeList = []
        for inventory in self.inventory_set.all():
            size = inventory.size
            if size not in sizeList:
                sizeList.append(size)
        return sizeList

    def getDetailList(self):
        import collections
        # 创建有序字典，用于存放详情信息（key:详情名称，value：图片列表）
        datas = collections.OrderedDict()
        for goodsdetail in self.goodsdetail_set.all():
            # 获取详情名称
            gdname = goodsdetail.name()
            if not datas.has_key(gdname):
                datas[gdname] = [goodsdetail.gdurl]
            else:
                datas[gdname].append(goodsdetail.gdurl)
        return datas


class GoodsDetailName(models.Model):
    gdname = models.CharField(max_length=30)

    def __str__(self):
        return self.gdname


class GoodsDetail(models.Model):
    gdurl = models.ImageField(upload_to='')
    gdname = models.ForeignKey(GoodsDetailName)
    goods = models.ForeignKey(Goods)

    def name(self):
        '''
        获取详情名称
        :return:
        '''
        return self.gdname.gdname


class Size(models.Model):
    sname = models.CharField(max_length=10)

    def __str__(self):
        return self.sname


class Color(models.Model):
    cname = models.CharField(max_length=10)
    colorurl = models.ImageField(upload_to='color/')

    def __str__(self):
        return self.cname


class Inventory(models.Model):
    count = models.PositiveIntegerField()
    color = models.ForeignKey(Color)
    goods = models.ForeignKey(Goods)
    size = models.ForeignKey(Size)

    class Meta:
        # 表备注
        verbose_name = '库存表'
