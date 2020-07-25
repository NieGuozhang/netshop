# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from django.urls import reverse
from django.views import View

from cart.cartmanager import *
from userapp.models import UserInfo, Area, Address
from utils.code import *


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        # 获取请求参数
        uname = request.POST.get('uname', '')
        pwd = request.POST.get('pwd', '')

        # 插入数据
        user = UserInfo.objects.create(uname=uname, pwd=pwd)
        if user:
            # 将用户信息存放至Session对象中
            request.session['user'] = user
            return redirect(reverse('user:center'))
        return redirect(reverse('user:register'))


class LoginView(View):
    def get(self, request):
        # 获取请求参数
        red = request.GET.get('redirect', '')

        data = {
            "redirect": red,
        }
        return render(request, 'login.html', context=data)

    def post(self, request):
        # 获取参数
        uname = request.POST.get('uname', '')
        pwd = request.POST.get('pwd', '')
        # 查询对象
        userList = UserInfo.objects.filter(uname=uname, pwd=pwd)

        # 判断对象是否存在
        if userList:
            request.session['user'] = userList[0]
            red = request.POST.get('redirect')

            # 判断重定向类型
            if red == 'cart':
                # 将Session中的购物项移动到数据库
                SessionCartManager(request.session).migrateSession2DB()
                return redirect(reverse('cart:query_cart_list'))
            elif red == 'order':
                return redirect(reverse('order:oder_list') + '?cartitems=' + request.POST.get('cartitems', ''))
            return redirect(reverse('user:center'))
        return redirect(reverse('user:login'))


class CheckUnameView(View):
    def get(self, request):
        # 获取请求参数
        uname = request.GET.get('uname', '')

        # 根据用户名去数据库中查询
        userList = UserInfo.objects.filter(uname=uname)
        flag = False

        # 判断是否存在
        if userList:
            flag = True
        return JsonResponse({'flag': flag})


class CenterView(View):
    def get(self, request):
        return render(request, 'center.html')


class LogoutView(View):
    def post(self, request):
        # 删除Session中所有数据（登录用户信息）
        if 'user' in request.session:
            del request.session['user']
        return JsonResponse({'delflag': True})


class LoadCodeView(View):
    def get(self, request):
        img, str = gene_code()
        request.session['code'] = str
        return HttpResponse(img, content_type='image/png', )


class CheckCodeView(View):
    def get(self, request):
        # 获取输入框中的验证码
        code = request.GET.get('code', '')
        session_code = request.session.get('code', None)

        checkFlag = code == session_code
        return JsonResponse({'checkFlag': checkFlag})


class AddressView(View):
    def get(self, request):
        user = request.session.get('user', '')
        addrList = user.address_set.all()
        data = {
            "addList": addrList,
        }
        return render(request, 'address.html', context=data)

    def post(self, request):
        flag = request.POST.get('flag', '')
        if flag == 'delete':
            id = request.get('addressid')
            address = Address.objects.get(id=id)
            # print(id + 'nnnnnnnn')
            if address:
                address.delete()
            user = request.session.get('user', '')
            addrList = user.address_set.all()
            data = {
                "addList": addrList,
            }
            return render(request, 'address.html', context=data)
        # 获取请求参数
        aname = request.POST.get('aname', '')
        aphone = request.POST.get('aphone', '')
        addr = request.POST.get('addr', '')
        user = request.session.get('user', '')

        # 将数据插入数据库
        address = Address.objects.create(aname=aname, aphone=aphone, addr=addr, userinfo=user,
                                         isdefault=(lambda count: True if count == 0 else False)(
                                             user.address_set.all().count()))
        # 获取当前用户所有的收获地址
        addrList = user.address_set.all()
        data = {
            "addList": addrList,
        }
        return render(request, 'address.html', context=data)


class LoadAreaView(View):
    def get(self, request):
        # 获取请求参数
        pid = request.GET.get('pid', '-1')
        pid = int(pid)

        # 根据父ID查询区划信息
        areaList = Area.objects.filter(parentid=pid)

        # 进行序列化
        jareaList = serialize('json', areaList)
        return JsonResponse({'jareaList': jareaList})


class DeleteAddressView(View):
    def get(self, request):
        id = request.GET.get('addrId', '')
        id = int(id)
        addr = Address.objects.get(id=id)
        if addr:
            addr.delete()
        return redirect(reverse('user:address'))
