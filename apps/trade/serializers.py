#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# Author:fsh
# time:'2018/4/1 21:51:12下午'
import time, random
from rest_framework import serializers
from goods.models import Goods
from goods.serializers import GoodsSerializer
from .models import ShoppingCart, OrderInfo, OrderGoods
from utils.alipay import AliPay
from MxShop.settings import private_key_path,ali_key_path
class ShopCatDetailSerializers(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)  # 外键对应只有一个

    class Meta:
        model = ShoppingCart
        fields = '__all__'


class ShopCatSerializer(serializers.Serializer):
    '''
    Serializer用起来比较灵活
    '''
    user = serializers.HiddenField(
        # 获取当前用户
        default=serializers.CurrentUserDefault()
    )
    nums = serializers.IntegerField(required=True, min_value=1, error_messages={
        'min_value': '商品数量不能小于1',
        'required': '请选择购买数量'
    })
    # 当你选择ModelSerializer就不用指定queryset
    goods = serializers.PrimaryKeyRelatedField(queryset=Goods.objects.all(),
                                               required=True)  # many=True是否包含多个,Goods是他的外键所指的model

    def create(self, validated_data):
        user = self.context['request'].user  # context上下文,在serializer不能直接self.request,user
        nums = validated_data['nums']
        goods = validated_data['goods']
        existed = ShoppingCart.objects.filter(user=user, goods=goods)

        if existed:
            # 如果数据库查询到该商品，就对他的数量进行更新
            existed = existed[0]
            existed.nums += nums
            existed.save()

        else:
            # 如果查询不到就创建
            existed = ShoppingCart.objects.create(**validated_data)
        return existed

    def update(self, instance, validated_data):
        '''
        更新操作
        :param instance:
        :param validated_data:
        :return:
        '''
        instance.nums = validated_data['nums']
        instance.save()
        return instance


class OrderGoodsSerializers(serializers.ModelSerializer):
    # OrderGoods序列号这个models
    goods = GoodsSerializer(many=False)

    class Meta:
        model = OrderGoods
        fields = '__all__'


class OrderDetailSerializers(serializers.ModelSerializer):
    #many=True OrderGoodsSerializers序列后是订单列表，可能包含多个商品，所以many允许多项
    goods = OrderGoodsSerializers(many=True)  # 反序列化 获取OrderGoodsSerializers序列化后的数据，嵌套进去
    #order = models.ForeignKey(OrderInfo,verbose_name='订单信息',related_name='goods') related_name必须填写才能反向引用
    alipay_url = serializers.SerializerMethodField(read_only=True)

    # many=True GoodsSerializer序列后是商品详情，详情只能有一个，所以many不允许多项
    def get_alipay_url(self, obj):
        # SerializerMethodField 字段 以get开头的函数，会自己来查找
        alipay = AliPay(
            appid='2016091000481624',
            app_notify_url="http://118.24.154.138:8001/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://118.24.154.138:8001/alipay/return/"
        )
        url = alipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount,

        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
        return re_url
    class Meta:
        model = OrderInfo
        fields = '__all__'


class OrderSerializers(serializers.ModelSerializer):
    def validate(self, attrs):
        attrs['order_sn'] = self.generate_order_sn()
        return attrs

    user = serializers.HiddenField(
        # 获取当前用户
        default=serializers.CurrentUserDefault()
    )
    order_sn = serializers.CharField(read_only=True)
    pay_status = serializers.CharField(read_only=True)  # read_only只读
    trade_no = serializers.CharField(read_only=True)
    pay_time = serializers.CharField(read_only=True)
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self,obj):
        alipay = AliPay(
            appid='2016091000481624',
            app_notify_url="http://118.24.154.138:8001/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://118.24.154.138:8001/alipay/return/"
        )
        url = alipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount,

        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
        return re_url

    class Meta:
        model = OrderInfo
        fields = '__all__'

    def generate_order_sn(self):
        '''
        生成订单号 (当前时间（精确到秒）+user_id+随机数)
        '''
        random_ins = random.Random()
        order_sn = "{time_str}{user_id}{ran_str}".format(time_str=time.strftime('%Y%m%d%H%M%S'),
                                                         user_id=self.context['request'].user.id,
                                                         ran_str=random_ins.randint(10, 99)
                                                         )
        return order_sn
