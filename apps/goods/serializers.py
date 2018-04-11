#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# Author:fsh
# time:'2018/3/14 22:01:35下午'
from rest_framework import serializers
from django.db.models import Q
from goods.models import Goods, GoodsCategory, GoodsImage, Banner, GoodsCategoryBrand,IndexAdd


# class GoodsSerializer(serializers.ModelSerializer):
#     name = serializers.CharField(required=True,max_length=100)
#     click_num = serializers.IntegerField(default=0)
#     goods_front_image = serializers.ImageField()
#
#     def create(self, validated_data):
#         """
#         Create and return a new `Snippet` instance, given the validated data.
#         """
#         #覆盖create 处理前端传过来的json数据
#         #objects model管理器
#         # 验证前端传的json的body
#         return Goods.objects.create(**validated_data)
class CategorySerializer3(serializers.ModelSerializer):
    class Meta:
        # 嵌套serializer,去外键完整信息
        model = GoodsCategory
        # fields = ('name','click_num','market_price','add_time')
        fields = '__all__'  # 获取所有字段


class CategorySerializer2(serializers.ModelSerializer):
    sub_cat = CategorySerializer3(many=True)  # many可能有多个

    class Meta:
        # 嵌套serializer,去外键完整信息
        model = GoodsCategory
        # fields = ('name','click_num','market_price','add_time')
        fields = '__all__'  # 获取所有字段


class CategorySerializer(serializers.ModelSerializer):
    sub_cat = CategorySerializer2(many=True)  # many可能有多个

    class Meta:
        # 嵌套serializer,去外键完整信息
        model = GoodsCategory
        # fields = ('name','click_num','market_price','add_time')
        fields = '__all__'  # 获取所有字段


class GoodsImaheSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = ('image',)


class GoodsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()  # 直接覆盖之前的category,实现取到外键的所有信息
    images = GoodsImaheSerializer(many=True)  # many外键必须指定，数据可能存在多条

    class Meta:
        model = Goods
        # fields = ('name','click_num','market_price','add_time')
        fields = '__all__'


# class GoodCategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = GoodsCategory
#         fields ="__all__"

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'


class BrandsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategoryBrand
        fields = '__all__'


class IndexCategorySerializer(serializers.ModelSerializer):
    brands = BrandsSerializer(many=True)
    goods = serializers.SerializerMethodField()
    sub_cat = CategorySerializer2(many=True)
    ad_goods = serializers.SerializerMethodField()

    def get_ad_goods(self,obj):
        goods_json = {}
        ad_goods = IndexAdd.objects.filter(category_id=obj.id)
        if ad_goods:
            goods_ins = ad_goods[0].goods
            goods_json = GoodsSerializer(goods_ins,many=False,context={'request':self.context['request']}).data

        return goods_json
    def get_goods(self, obj):
        all_goods = Goods.objects.filter(Q(category_id=obj.id) | Q(category__parent_category_id=obj.id) | Q(
            category__parent_category__parent_category_id=obj.id))
        goods_serializer = GoodsSerializer(all_goods, many=True,context={'request':self.context['request']})
        return goods_serializer.data

    class Meta:
        model = GoodsCategory
        fields = '__all__'


