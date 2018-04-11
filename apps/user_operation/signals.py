#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# Author:fsh
#time:'2018/3/29 23:15:14下午'
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

# User = get_user_model()
from user_operation.models import UserFav

@receiver(post_save, sender=UserFav)
def create_user_fav(sender, instance=None, created=False, **kwargs):
    #需要重载apps下面的read函数  用来接受信号的 post save 的信号 使用信号会增加代码的分离性
    if created:
        goods = instance.goods
        goods.fav_num+=1 #收藏+1
        goods.save()

@receiver(post_delete,sender=UserFav)
def deleted_user_fav(sender,instance=None,create=False,**kwargs):
    goods = instance.goods
    goods.fav_num -= 1  # 收藏+1
    goods.save()
