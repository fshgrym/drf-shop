from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
# Create your views here.
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from .serializers import UserFavSerializers, LeavingMessageSerializer,AddressSerializer
from .models import UserFav, UserLeavingMessage,UserAddress
from utils.permissions import IsOwnerOrReadOnly
from .serializers import UserFavDetailSerializer


class UserFavViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin, viewsets.GenericViewSet):
    '''
    list:
        用户收藏列表
    retrieve:
        判断某个商品是否收藏
    create:
        用户添加收藏
    delete:
        取消收藏
    '''
    # IsAuthenticated判断是否登录
    # queryset = UserFav.objects.all()
    # serializer_class = UserFavSerializers
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    # 全局配置token会导致token失效访问不了
    lookup_field = "goods_id"  # ，默认是pk

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)
    # def perform_create(self, serializer):
    #     instance = serializer.save()
    #     goods = instance.goods
    #     goods.fav_num+=1 #收藏+1 这里我们采用了发送信号的方式来完成
    #     goods.save()

    def get_serializer_class(self):
        # 重载get_serializer_class,用来动态serializer设置
        if self.action == 'list':  # 当你使用ViewSet才有的self.action
            # 如果是获取用户详情就使用UserDetailSerializer这个序列类
            return UserFavDetailSerializer
        elif self.action == 'create':
            # 如果是其他情况就是UserDetailSerializer
            return UserFavSerializers
        return UserFavSerializers


class LeavingMessingViewSet(mixins.ListModelMixin, mixins.DestroyModelMixin, mixins.CreateModelMixin,
                            viewsets.GenericViewSet):
    '''
     list:
         获取留言
     create:
         添加留言
     delete:
         删除留言
    '''
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = LeavingMessageSerializer

    def get_queryset(self):
        # 默认查询当前用户的所有信息留言
        return UserLeavingMessage.objects.filter(user=self.request.user)


# class AddressViewSet(mixins.ListModelMixin, mixins.DestroyModelMixin,mixins.UpdateModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
class AddressViewSet(viewsets.ModelViewSet):#ModelViewSet增删改查全部实现了
    '''
    收货地址管理
    list:
    获取收货地址
    create:
    新建收货地址
    update:
    更新收货地址
    delete:
    删除收货地址

    '''
    serializer_class = AddressSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)