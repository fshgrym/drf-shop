from random import choice
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from rest_framework.mixins import CreateModelMixin
from rest_framework import viewsets, status,mixins
from rest_framework import permissions
from rest_framework import authentication
from rest_framework.response import Response
from rest_framework_jwt.serializers import jwt_encode_handler,jwt_payload_handler
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .models import VerifyCode
from MxShop.settings import YUN_PIAN_API_KEY

from utils.yunpian import YunPian

# Create your views here.

User = get_user_model()
from .serializers import SmsSerializer, UserRegSerializer,UserDetailSerializer


class CustomBackend(ModelBackend):  # 会调用我门写的login的views函数
    '''
    自定义认证View,支持手机号码登录
    如果想自定义认证
        1、继承ModelBackend
        2、重写authenticate
        3、setting添加AUTHENTICATION_BACKENDS
    '''

    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewSet(CreateModelMixin, viewsets.GenericViewSet):
    '''
    发送短信验证码
    '''
    serializer_class = SmsSerializer

    # 重写CreateModelMixin的create
    def generate_code(self):
        '''
        生成随机的code验证吗
        :return:
        '''
        seeds = '1234567890'
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))  # 随机取一个
        return ''.join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # 调用失败就会被drf捕捉到

        mobile = serializer.validated_data['mobile']
        code = self.generate_code()
        yun_pian = YunPian(YUN_PIAN_API_KEY)
        sms_status = yun_pian.send_sms(code=code, mobile=mobile)
        if sms_status['code'] != 0:
            # code等于0成功，其他则出错
            return Response(sms_status['msg'], status.HTTP_400_BAD_REQUEST)
        else:
            # 验证通过，保存到数据库
            code_record = VerifyCode(code=code, mobile=mobile)
            code_record.save()
            return Response({'mobile': mobile}, status.HTTP_201_CREATED)

            # self.perform_create(serializer)
            # headers = self.get_success_headers(serializer.data)
            # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserViewSet(CreateModelMixin,mixins.UpdateModelMixin,mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    create:
        注册用户
    '''
    # mixins.UpdateModelMixin 更新操作 CreateModelMixin新建 RetrieveModelMixin详情
    # serializer_class = UserRegSerializer
    queryset = User.objects.all()
    #登录认证
    authentication_classes = (JSONWebTokenAuthentication,authentication.SessionAuthentication,)
    # permission_classes = ('',)权限控制
    def get_serializer_class(self):
        #重载get_serializer_class,用来动态serializer设置
        if self.action == 'retrieve':#当你使用ViewSet才有的self.action
            #如果是获取用户详情就使用UserDetailSerializer这个序列类
            return UserDetailSerializer
        elif self.action == 'create':
            #如果是其他情况就是UserDetailSerializer
            return UserDetailSerializer
        return UserDetailSerializer
    def get_permissions(self):
        #重载APIview的get_permissions,用来动态权限设置
        if self.action == 'retrieve':#当你使用ViewSet才有的self.action
            #如果是获取用户详情就需要登录
            return [permissions.IsAuthenticated()]
        elif self.action == 'create':
            #如果是注册则不需要登录
            return []
        return []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)#raise_exception报错会被drf捕捉
        user = self.perform_create(serializer)

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict['token'] = jwt_encode_handler(payload)
        re_dict['name'] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)
    def get_object(self):
        #控制mixin.RetrieveModelMixin
        return self.request.user
    def perform_create(self, serializer):
        return serializer.save()
