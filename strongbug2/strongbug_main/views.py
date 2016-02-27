# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib.auth.hashers import make_password,check_password
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from redis_tool import main
from tool_base import token_auth
from django import forms
import time
import os
import hashlib
import commands
import json
import docker
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import models
def index(request):
    page= request.GET.get('page')
    soso= request.GET.get('q')

    if not page:
        page=1
    list=models.Wtstitle.objects.order_by('-id').all()[int(page)*15-15:int(page)*15]
    ret={}
    dataList=[]
    for i in list:
        datadic={}
        datadic['title']=i.title_c
        datadic['click_ip']=i.click_ip
        datadic['auth']=i.auth
        datadic['time']=i.time
        datadic['md5']=i.md5
        datadic['reply_mun']=i.reply_mun
        datadic['id']=i.id


        dataList.append(datadic)
    if not page:
        page=0
    ret['pagen']=int(page)+1
    if int(page)>1:
         ret['pagel']=int(page)-1
    else:
            ret['pagel']=int(page)
    ret['data']=dataList
    ret['page']=int(page)
    if soso:
        return HttpResponseRedirect("/soso"+"&q="+str(soso))
    return render_to_response('strongbug.html',ret,context_instance=RequestContext(request))

def bug_index(request,page):
    if page:
        index=models.Wtstitle.objects.filter(id=int(page))[0]
        ret={}
        ret['content']=index.content
        ret['click_ip']=index.click_ip
        ret['auth']=index.auth
        ret['time']=index.time
        ret['title']=index.title_c
        ret['reply_mun']=index.reply_mun
        list=models.WtsComments.objects.filter(proo_id=int(page))
        dl=[]
        for i in list:
            d={}
            d['content']=i.content
            d['auth']=i.auth
            d['time']=i.time
            dl.append(d)
        ret['data']=dl
        return render_to_response('strongbug6.html',ret,context_instance=RequestContext(request))


def soso(request):
    page= request.GET.get('page')
    soso= request.GET.get('q')

    if not soso:
        soso='python'
    if not page:
        page=1
    list=models.Wtstitle.objects.filter(content__icontains=soso)[int(page)*15-15:int(page)*15]
    ret={}
    dataList=[]
    for i in list:
        datadic={}
        datadic['title']=i.title_c
        datadic['click_ip']=i.click_ip
        datadic['auth']=i.auth
        datadic['time']=i.time
        datadic['md5']=i.md5
        datadic['reply_mun']=i.reply_mun
        datadic['id']=i.id


        dataList.append(datadic)
    if not page:
        page=0
    ret['pagen']=int(page)+1
    if int(page)>1:
         ret['pagel']=int(page)-1
    else:
            ret['pagel']=int(page)
    ret['data']=dataList
    ret['page']=int(page)
    ret['so']='?q='+soso
    return render_to_response('strongbug.html',ret,context_instance=RequestContext(request))

def s(request):
    return HttpResponse('404')

def registered(request):
    m2 = hashlib.md5()
    m2.update(str(time.time()))
    tk=m2.hexdigest()
    print(tk)
    img_path_json=token_auth.token_auth_img(str(tk))
    imgs=img_path_json
    print(imgs)
    main.mains().Set(str(imgs['img_path']),str(imgs['token']))
    ret={}
    ret['path']=str(imgs['img_path'])
    return render_to_response('strongbug2.html',ret,context_instance=RequestContext(request))
def logins(request):

    return render_to_response('index.html')

def logout_view(request):
    logout(request)
    return index(request)
def zhuce(request):

    username=request.POST.get('username')
    password=request.POST.get('password')
    email=request.POST.get('email')

    code=request.POST.get('code')
    p=request.POST.get('c')
    print(code,main.mains().Get(str(code)))
    if str(main.mains().Get(str(code)))!=str(p):
        return HttpResponse('验证码不正确')
    if User.objects.filter(username=username):
        return HttpResponse('用户名已存在')
    if User.objects.filter(email=email):
        return HttpResponse('email已存在')
    if username and password is not None:
        user = User.objects.create_user(username=username,password=password,email=email)
        if not user.is_staff:
            user.save()
        else:
            return HttpResponse('用户名已存在')



        return logins(request)


    else:
        return HttpResponse('password and uasename is not None~~')


def login_view(request):


    username=request.POST.get('username')
    password=request.POST.get('password')
    print(password)
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            return HttpResponse('password and uasename is not error~~')
    else:
        return HttpResponse('password and uasename is not None~~')


# coding: utf-8

from django.http import HttpResponse
from PIL import ImageFile


import django.forms as forms

class PictureForm(forms.Form):
    # ......
    # 图片
    imagefile = forms.ImageField()
    # ......

def addPicture(request):
        print request.method
        form = PictureForm(request.POST, request.FILES)
        print 1

        f = request.FILES.get("imagefile")
        print 2
        parser = ImageFile.Parser()
        for chunk in f.chunks():
            parser.feed(chunk)
        img = parser.close()
        # 在img被保存之前，可以进行图片的各种操作，在各种操作完成后，在进行一次写操作
        img.save("static/22.jpg")

def handle_uploaded_file(f):
    with open('static/2.jpg', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()



class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

def upload_file(request):

     form = UploadFileForm(request.POST, request.FILES)

     handle_uploaded_file(request.FILES.get('imagefile'))
     return HttpResponseRedirect('/')
def handle_uploaded_files(request):
    import subprocess
    c = docker.Client(base_url='unix://var/run/docker.sock',timeout=10)
    c.start(container='b7a44f337998')


    
    print 11
    #s=commands.getstatusoutput('cd /')

    s2=commands.getstatusoutput('docker start -i swing')

    print 22
    s3=commands.getstatusoutput('docker run -it -v /home/dataswing:/ddata  ubuntu /bin/bash')

    s4=commands.getstatusoutput('cd /home')

    s5=commands.getstatusoutput('mkdir /home/swings')
    file_name = "ss.jpg"
    print 33
    f = request.FILES["file"]


    path = "/ddata/"


    file_name = path + file_name
    destination = open(file_name, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()


    return HttpResponseRedirect('/')

