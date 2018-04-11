#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# Author:fsh
# time:'2018/3/28 21:39:09下午'
import re
from datetime import datetime, timedelta
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model

User = get_user_model()
from MxShop.settings import REGEX_MOBILE
from .models import VerifyCode


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11,help_text='手机号码')

    # 验证手机号码，单独继承validate_mobile
    def validate_mobile(self, mobile):
        '''
        验证手机号码
        :param mobile:
        :return:
        '''

        # 手机号码是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError('号码已经注册')
        # 验证手机号码是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError('手机号码非法')
        # 验证频率的限制
        one_min_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)  # 当前时间减去一分钟前
        if VerifyCode.objects.filter(add_time__gt=one_min_ago, mobile=mobile):  # 添加时间大于一分钟之前的时间
            raise serializers.ValidationError('距离上一次发送未超过60s')
        return mobile

class UserDetailSerializer(serializers.ModelSerializer):
    '''
    用户详情信息序列化
    '''
    class Meta:
        model = User
        fields = ('name', 'gender','birthday', 'mobile', 'email')
class UserRegSerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=4, min_length=4, required=True, help_text='验证码', write_only=True,
                                 label='验证码',
                                 error_messages={
                                     'blank': '请输入验证码',
                                     'required': '请输入验证码',
                                     'max_length': '验证码格式错误',
                                     'min_length': '验证码格式错误'

                                 }
                                 )
    username = serializers.CharField(required=True, allow_blank=False, label='用户名',help_text='用户名',
                                     validators=[UniqueValidator(queryset=User.objects.all(), message='用户已经存在')])
    password = serializers.CharField(
        style={'input_type': 'password'}, label='密码', write_only=True,help_text='密码',
    )

    def create(self, validated_data):
        user = super(UserRegSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate_code(self, code):
        # initial_data 用户post的数据会放在这里面 ，按时间排序验证码最后发送的有效
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data['username']).order_by('-add_time')
        if verify_records:
            last_record = verify_records[0]
            five_min_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)  # 当前时间减去五分钟分钟前
            if five_min_ago > last_record.add_time:
                raise serializers.ValidationError('验证码过期')
            if last_record.code != code:
                raise serializers.ValidationError('验证码错误')
        else:
            raise serializers.ValidationError('验证码错误')

    def validate(self, attrs):
        '''作用于serializers所有的字段上 attrs所有字段返回的dict'''
        attrs['mobile'] = attrs['username']  # 添加字段使用户名和手机号码一致
        del attrs['code']  # 删除code,已经存在数据库，只为验证
        return attrs

    class Meta:
        model = User
        fields = ('username', 'code', 'mobile', 'password')
