# -*- coding: utf-8 -*-

import datetime
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseForbidden
from dateutil import tz
from user.models import User

# Create your views here.

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user_obj = User.objects.filter(username=username,
                                           password=password).first()
            if user_obj:
                return HttpResponse('登陆成功')
            return HttpResponse('帐号或密码不正确')
        return HttpResponse('帐号或密码内容不能为空')
    return Http404()


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        #signup_time = datetime.datetime.now(tz=timezone.utc)
        signup_time = datetime.datetime.now(tz=tz.gettz('Asia/Shanghai'))
        print(username, password, password2, email, phone, signup_time)
        if username and password and password2 and email and phone:
            if password != password2:
                return HttpResponse(content='两次密码不一致')

            user_obj = User.objects.filter(username=username).first()
            if user_obj:
                return HttpResponse(content='用户已存在')

            User.objects.create(username=username,
                                password=password,
                                email=email,
                                phone=phone,
                                signup_time=signup_time).save()
            return HttpResponse(content='注册成功')
        return HttpResponseForbidden(content='参数有误')
    return Http404()
