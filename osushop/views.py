# from django.contrib.auth.models import User
import json
import logging
import os
import uuid

from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from django.db import DatabaseError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import *


# Create your views here.

def welcometoindex(request):
    user_id = request.session.get('user_id')
    nick_name = request.session.get('nick_name')
    # if user_id is not None:
    #     user = UserInfo.objects.get(id=user_id)
    #     # goods_list = GoodsInfo.objects.filter().exclude(user=user).order_by('-create_time')
    # else:
    #     pass# goods_list = GoodsInfo.objects.filter().order_by('-create_time')
    goods_list = GoodsInfo.objects.filter().order_by('-create_time')
    return render(request, 'index.html', {"goods_list": goods_list, "nick_name": nick_name})


def register(request):
    flag = ""
    if request.method == 'POST':
        new_user = UserInfo()

        user_name = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if user_name == "":
            flag = "Please input your user name! "
            return render(request, 'register.html', {"flag": flag})
        else:
            if email == "":
                flag = "Please input your email! "
                return render(request, 'register.html', {"flag": flag})
            else:
                if password1 == "":
                    flag = "Please input your password! "
                    return render(request, 'register.html', {"flag": flag})
                else:
                    if password2 == "":
                        flag = "Please input your password again! "
                        return render(request, 'register.html', {"flag": flag})


        # check if user name is used
        new_user.nick_name = user_name
        name_checker = UserInfo.objects.filter(nick_name=new_user.nick_name)
        if len(name_checker) > 0:
            return render(request, 'register.html', {"flag": "this name already exists"})

        if password1 != password2:
            return render(request, "register.html", {"flag": "passwords not match"})

        new_user_pwd = make_password(password1, 'abc', 'pbkdf2_sha1')
        new_user.password = new_user_pwd
        new_user.email = email
        try:
            new_user.save()
            flag = 'success'
        except DatabaseError as e:
            logging.warning(e)
        return render(request, 'index.html', {"message": "Register Successfully!"})

    return render(request, 'register.html', {"flag": flag})


@csrf_exempt
def login(request):
    flag = 0
    user = UserInfo()
    if request.method == 'POST':
        user_email = request.POST.get('email')
        user_password = request.POST.get('password')
        if user_email == 'supper@qq.com' and user_password == '123456':
            flag = 5
            return HttpResponse(flag)
        else:
            try:
                user = UserInfo.objects.get(email=user_email)
                print(user.__str__())
            except Exception as e:
                print(e.__repr__())
                flag = -1
            if user is None:  # 用户名不存在
                return HttpResponse(flag)
            if check_password(user_password, user.password):  # 密码相等，登录成功
                flag = 1
                request.session['nick_name'] = user.nick_name
                request.session['user_id'] = user.id
            else:  # 密码错误
                flag = 2
            return HttpResponse(flag)
    return render(request, 'login.html')

def workingon(request):
    return  render(request, "workingon.html")

def logout(request):
    del request.session["nick_name"]
    del request.session["user_id"]
    return HttpResponseRedirect("index")


@csrf_exempt
def issue_form(request):
    flag = 0
    nick_name = request.session.get('nick_name')
    if request.method == "POST":
        # 里面的参数是name
        goods_name = request.POST.get("goods_name")
        print(goods_name)
        goods_detail = request.POST.get("goods_detail")
        print(goods_detail)
        goods_price = request.POST.get("goods_price")
        print(goods_price)
        category = request.POST.get("category")
        print(category)
        transactionMode = request.POST.get("transactionMode")
        print(transactionMode)
        pho_num = request.POST.get("pho_num")
        print(pho_num)
        email = request.POST.get("email")
        print(email)
        file_img = request.FILES.get('file_img')
        print(file_img.name)
        print(file_img.size)
        file_chunks = file_img.chunks()
        # 文件保存的路径
        # /images/qwyuqguweuq.jpg
        file_name = do_file_name(file_img.name)
        # 完整的路径
        store_path = os.path.join(settings.MEDIA_ROOT, "img")
        file_path = os.path.join(store_path, file_name).replace('\\', '/')

        new_issue = GoodsInfo()
        new_issue.name = goods_name
        new_issue.detail = goods_detail
        new_issue.price = goods_price
        new_issue.master_pho = pho_num
        new_issue.master_email = email
        new_issue.trading = transactionMode
        # if not a registered user, register  暂时没做
        # user_id = request.session.get('user_id')
        # new_issue.user_id = UserInfo.objects.get(id=user_id)
        # sort = SortInfo.objects.get(id=category)
        # print(sort.__dict__)
        new_issue.sort_id = category
        new_issue.img = file_name
        try:
            new_issue.save()
            with open(file_path, "wb")as file:
                for chunk in file_chunks:
                    file.write(chunk)
            flag = 1
        except Exception as e:
            print(e)
        return HttpResponse(flag)
    return render(request, "issue_page.html", {"nick_name": nick_name})


# generate different pic name
def do_file_name(file_name):
    return str(uuid.uuid1()) + os.path.splitext(file_name)[1]


def togood_detail_page(request):
    nick_name = request.session.get('nick_name')
    id = request.GET.get('id')
    print("id: " + id)
    goods_detal = GoodsInfo.objects.get(id=id)
    return render(request, "good_detail_page.html", {"goods_detail": goods_detal, "nick_name": nick_name})


def search(request):
    flag = 1
    key = request.GET.get("key")
    # print("key" + key)
    nick_name = request.session.get('nick_name')
    goods_list = GoodsInfo.objects.filter(name__contains=key).order_by('-create_time')
    return render(request, 'index.html', {"goods_list": goods_list, "nick_name": nick_name})


def search2(request):
    flag = 1
    key = request.GET.get("sort_id")
    # print("key" + key)
    nick_name = request.session.get('nick_name')
    goods_list = GoodsInfo.objects.filter(sort_id=key).order_by('-create_time')
    return render(request, 'index.html', {"goods_list": goods_list, "nick_name": nick_name})


def join_cart(request):
    result = 2
    good_id = request.GET.get("id")

    # good = Goods()
    # good = Goods.objects.get(id=good_id)
    # cart_check = Cart()
    # cart_check = Cart.objects.get(goods=good)
    # if cart_check is not None:
    #     result = 2
    #     return HttpResponse(json.dumps(result))
    user_id = request.session.get('user_id')
    print(user_id)
    cart = CartInfo()
    cart.user_id = user_id
    cart.goods_id = good_id
    try:
        cart.save()
    except Exception:
        print(Exception)
        result = 0
    return HttpResponse(json.dumps(result))