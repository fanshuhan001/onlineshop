from django.db import models


# from User.models import Us


# Create your models here.
class GoodsInfo(models.Model):
    # db_table = 'goods'
    id = models.AutoField(primary_key=True)
    img = models.CharField(max_length=255)
    sort_id = models.BigIntegerField()
    name = models.CharField(max_length=255)
    detail = models.TextField(max_length=255, blank=True, default="no more description for this item now")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    trading = models.SmallIntegerField()  # three trading methods
    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)
    master_pho = models.CharField(max_length=255, blank=True, null=True)
    master_email = models.EmailField(blank=False)
    user_id = models.BigIntegerField(null=True)


class UserInfo(models.Model):
    # db_table = 'user'
    id = models.AutoField(primary_key=True)
    nick_name = models.CharField(max_length=30, null=False)
    # detail_info = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, blank=True)
    img = models.ImageField(max_length=255, blank=True)
    phone_num = models.CharField(max_length=15, blank=True)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    sex = models.BooleanField(default=0)  # 0 male
    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)


class CartInfo(models.Model):
    # db_table = 'cart'
    id = models.AutoField(primary_key=True)
    user_id = models.BigIntegerField()
    goods_id = models.BigIntegerField()
    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)


# category(fixed)
class SortInfo(models.Model):
    # db_table = 'sort'
    id = models.AutoField(primary_key=True)
    sort_name = models.CharField(max_length=255)
    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)
