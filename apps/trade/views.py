from datetime import datetime
from django.shortcuts import redirect
from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import mixins, viewsets, permissions
from MxShop.settings import ali_key_path,private_key_path
from .serializers import ShopCatSerializer,ShopCatDetailSerializers,OrderSerializers,OrderDetailSerializers
from utils.permissions import IsOwnerOrReadOnly
from .models import ShoppingCart,OrderInfo,OrderGoods
from utils.alipay import AliPay
# Create your views here.
class ShoppingCatViewSet(viewsets.ModelViewSet):
    '''
    购物车功能开发
    list:
    获取购物车列表
    create:
    添加购物车

    '''

    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    # serializer_class = ShopCatSerializer

    # queryset = ShoppingCart.objects.all()
    lookup_field = 'goods_id'

    def get_serializer_class(self):
        if self.action == 'list':
            return ShopCatDetailSerializers
        else:
            return ShopCatSerializer

    def perform_create(self, serializer):
        #商品库存数量修改，这里是加到购物车就减少相应数量
        shop_cat = serializer.save()
        goods = shop_cat.goods
        goods.goods_num -= shop_cat.nums
        goods.save()
    def perform_destroy(self, instance):
        #删除购物车，增加相应的数量，这里有个细节，必须先取到商品再删除，否则找不到
        goods = instance.goods
        goods.goods_num += instance.nums
        goods.save()
        instance.delete()
    def perform_update(self, serializer):
        existed_record = ShoppingCart.objects.get(id=serializer.instance.id)
        existed_nums = existed_record.nums
        saved_record = serializer.save() #保存之后的值
        nums = saved_record.nums - existed_nums #保存之后的值减去保存之前的值，如果是整数就是加的操作
        goods = saved_record.goods
        goods.goods_num -= nums
        goods.save()
    def get_queryset(self):
        '''
        返回当前用户的所有
        :return:
        '''
        return ShoppingCart.objects.filter(user=self.request.user)

class OrderViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin,mixins.CreateModelMixin,viewsets.GenericViewSet):#订单是不可修改的
    '''
    订单管理
    list:
        获取订单列表
    create:
        添加订单
    delete:
        删除订单
    '''
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    # serializer_class = OrderSerializers
    lookup_field = 'id'
    def get_queryset(self):
        #获取当前用户的订单
        return OrderInfo.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderDetailSerializers
        return OrderSerializers
    def perform_create(self, serializer):
        order = serializer.save()
        shop_carts = ShoppingCart.objects.filter(user=self.request.user)
        for shop_cart in shop_carts:
            #保存购物车所有的商品
            order_goods = OrderGoods()
            order_goods.goods = shop_cart.goods
            order_goods.goods_num = shop_cart.nums
            order_goods.order = order
            order_goods.save()

            shop_cart.delete()#删除购物车商品
        return order

from rest_framework.views import APIView
class AliPayView(APIView):
    def get(self,request):
        '''
        处理支付宝return_url返回
        :param request:
        :return:
        '''
        processed_dict = {}
        for key, value in request.GET.items():
            processed_dict[key] = value
        sign = processed_dict.pop('sign', None)
        alipay = AliPay(
            appid='2016091000481624',
            app_notify_url="http://118.24.154.138:8001/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://118.24.154.138:8001/alipay/return/"
        )
        verify = alipay.verify(processed_dict, sign)  # 验证支付宝发过来的签名
        if verify is True:
            order_sn = processed_dict.get('out_trade_no', None)
            trade_no = processed_dict.get('trade_no', None)
            trade_status = processed_dict.get('trade_status', None)

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)  # 查询是否有这个订单
            for existed_order in existed_orders:
                existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()
            response = redirect("index")
            response.set_cookie("nextPath","pay", max_age=3)
            return response
        else:
            response = redirect("index")
            return response

    def post(self,request):
        '''
        处理支付宝notify_url,异步请求
        :param request:
        :return:
        '''
        processed_dict = {}
        for key, value in request.GET.items():
            processed_dict[key] = value
        sign = processed_dict.pop('sign', None)
        alipay = AliPay(
            appid='2016091000481624',
            app_notify_url="http://118.24.154.138:8001/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://118.24.154.138:8001/alipay/return/"
        )
        verify = alipay.verify(processed_dict, sign)  # 验证支付宝发过来的签名
        if verify is True:
            order_sn = processed_dict.get('out_trade_no', None)
            trade_no = processed_dict.get('trade_no', None)
            trade_status = processed_dict.get('trade_status', None)

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)  # 查询是否有这个订单
            for existed_order in existed_orders:

                order_goods = existed_order.goods.all()
                #商品售出数量计数
                for order_good in order_goods:
                    goods = order_good.goods
                    goods.sold_num += order_good.goods_num
                    goods.save()

                existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()
            response = redirect("index")
            response.set_cookie("nextPath","pay", max_age=3)
            return response
        else:
            response = redirect("index")
            return response

