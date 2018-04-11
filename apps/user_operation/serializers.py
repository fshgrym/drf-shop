#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# Author:fsh
# time:'2018/3/30 23:44:21下午'
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import UserFav, UserLeavingMessage, UserAddress
from goods.serializers import GoodsSerializer


class UserFavDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer()  # many=True因为它本身就是一个外键，不需要manay

    class Meta:  # goods字段名字
        model = UserFav
        fields = ('goods', 'id')


class UserFavSerializers(serializers.ModelSerializer):
    user = serializers.HiddenField(
        # 获取当前用户
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserFav
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),
                message='已经收藏'
            )
        ]
        # 加入id后删除功能才能实现
        fields = ('user', 'goods', 'id')


class LeavingMessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        # 获取当前用户
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')  # 只返回不提交 read_only

    class Meta:
        model = UserLeavingMessage
        fields = ('id', 'user', 'message_type', 'subject', 'message', 'file', 'add_time')


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
            # 获取当前用户
            default=serializers.CurrentUserDefault()
        )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = UserAddress
        fields = ('id', 'user', 'province', 'city', 'district', 'address', 'signer_name', 'signer_mobile', 'add_time')
