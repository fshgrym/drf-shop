#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# Author:fsh
#time:'2018/3/29 23:15:14下午'
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    #需要重载apps下面的read函数  用来接受信号的 post save 的信号
    if created:
        password = instance.password
        instance.set_password(password)
        instance.save()