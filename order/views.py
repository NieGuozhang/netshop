# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys

from django.db.models import F

from cart.models import CartItem
from goods.models import Inventory
from order.models import Order, OrderItem
from userapp.models import Address
from utils.alipay import AliPay

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
import jsonpickle

from cart.cartmanager import getCartManger

reload(sys)
sys.setdefaultencoding('utf8')


class ToOrderView(View):
    def get(self, request):
        # 获取请求参数
        cartitems = request.GET.get('cartitems', '')

        # 判断用户是否登录
        if not request.session.get('user'):
            return render(request, 'login.html', {'cartitems': cartitems, 'redirect': 'order'})
        return redirect(reverse('order:oder_list') + '?cartitems=' + cartitems)


class OrderListView(View):
    def get(self, request):
        # 获取请求参数
        cartitems = request.GET.get('cartitems', '')

        # 将Json格式字符串转化为Python对象（字典）列表
        cartitemList = jsonpickle.loads("[" + cartitems + "]")
        # print cartitemList

        # 将Python对象列表转化成CartItem对象
        cartitemObjList = [getCartManger(request).get_cartitems(**item) for item in cartitemList if item]

        # 获取用户的默认收货地址
        address = request.session.get('user').address_set.get(isdefault=True)

        # 获取支付的总金额
        totalPrice = 0
        for cm in cartitemObjList:
            totalPrice += cm.getTotalPrice()
        data = {
            'cartitemObjList': cartitemObjList,
            'address': address,
            'totalPrice': totalPrice,
        }
        return render(request, 'order.html', context=data)


# 创建Alipay对象
alipay = AliPay(appid='2016102500755406',
                app_notify_url='http://127.0.0.1:8000/order/checkPay/',
                app_private_key_path='order/keys/my_private_key.txt',
                alipay_public_key_path='order/keys/alipay_public_key.txt',
                return_url='http://127.0.0.1:8000/order/checkPay/',
                debug=True)


class ToPayView(View):
    def get(self, request):
        # 1.插入Order表中数据
        # 获取请求参数
        import uuid, datetime
        # print(request.GET.get('payway'))
        # print request.GET.get('address', '')
        date = {
            "out_trade_num": uuid.uuid4().get_hex(),
            "order_num": datetime.datetime.today().strftime('%Y%m%d%H%M%S'),
            "payway": request.GET.get('payway'),
            "address": Address.objects.get(id=request.GET.get('address', '')),
            "user": request.session.get('user', ''),
        }
        orderObj = Order.objects.create(**date)

        # 2.插入OrderItem表中数据
        cartitems = jsonpickle.loads(request.GET.get('cartitems'))

        orderItemList = [OrderItem.objects.create(order=orderObj, **item) for item in cartitems if item]

        totalPrice = request.GET.get('totalPrice')[1:]

        # 获取扫码支付请求参数
        params = alipay.direct_pay(subject='京东超市',
                                   out_trade_no=orderObj.out_trade_num,
                                   total_amount=str(totalPrice))

        # 获取扫码支付的请求地址
        url = alipay.gateway + "?" + params
        return redirect(url)


# 校验是否支付完成
class CheckPayView(View):
    def get(self, request):
        # 获取所有请求参数
        params = request.GET.dict()
        # print params

        # 获取签名
        sign = params.pop('sign')

        # 校验是否支付成功
        success = alipay.verify(params, sign)
        # print success
        if success:
            # 修改订单表中的支付状态
            out_trade_no = params.get('out_trade_no')
            order = Order.objects.get(out_trade_num=out_trade_no)
            order.status = u'等待发货'
            order.save()

            # 修改库存
            orderitemList = order.orderitem_set.all()

            [Inventory.objects.filter(goods_id=item.goodsid, size_id=item.sizeid, color_id=item.colorid).update(
                count=F('count') - item.count)
             for item in orderitemList if item]

            # 修改购物表
            [CartItem.objects.filter(goodsid=item.goodsid, sizeid=item.sizeid, colorid=item.colorid).delete() for item
             in orderitemList if item]

            return HttpResponse('支付成功！')
        return HttpResponse('支付失败！')
