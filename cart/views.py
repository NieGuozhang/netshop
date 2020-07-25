# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from django.views import View
from cartmanager import *


class AddCartView(View):
    def post(self, request):
        # 获取当前操作类型
        flag = request.POST.get('flag', '')

        # 判断当前操作类型
        if flag == 'add':
            # 在多级字典数据的时候，需要手动设置modified=True,实时地将数据存入到Session对象中
            request.session.modified = True
            # 创建cartManager对象
            cartManagerObj = getCartManger(request)
            # 加入购物车
            cartManagerObj.add(**request.POST.dict())
        elif flag == 'plus':
            # 创建cartManager对象
            cartManagerObj = getCartManger(request)
            # 更新购物车
            cartManagerObj.update(step=1, **request.POST.dict())
        elif flag == 'minus':
            # 创建cartManager对象
            cartManagerObj = getCartManger(request)
            # 更新购物车
            cartManagerObj.update(step=-1, **request.POST.dict())
        elif flag == 'delete':
            cartManagerObj = getCartManger(request)
            # 删除商品
            cartManagerObj.delete(**request.POST.dict())
        return redirect(reverse('cart:query_cart_list'))


class CartListView(View):
    def get(self, request):
        # 创建cartManager对象
        cartManagerObj = getCartManger(request)
        cartList = cartManagerObj.queryAll()
        data = {
            'cartList': cartList,
        }
        return render(request, 'cart.html', context=data)
