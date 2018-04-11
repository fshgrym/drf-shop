#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# Author:fsh
#time:'2018/3/15 22:25:59下午'
import django_filters
from .models import Goods
class ProductFilter(django_filters.rest_framework.FilterSet):
    '''
    商品的过滤类
    '''
    #lookup_expr 执行操作，会调用Goods.objects.filter(shop_price__gt=100)类似这样的操作
    pricemin = django_filters.NumberFilter(name='shop_price',lookup_expr='gte',help_text='最低价格')
    pricemax = django_filters.NumberFilter(name='shop_price',lookup_expr='lte',help_text='最高价格')
    name = django_filters.CharFilter(name='name',lookup_expr='icontains',help_text='商品名称')#模糊查询,i忽略大小写

    #自定义过滤器
    top_category = django_filters.NumberFilter(method='top_category_filter',help_text='获取顶级分类下所有分类')#method是自定义的函数
    def top_category_filter(self,queryset,name,value):
        #查询第一类目的所有商品或者二级类目
        from django.db.models import Q
        return queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) | Q(
            category__parent_category__parent_category_id=value))
    class Meta:
        model = Goods
        fields = ['pricemin', 'pricemax','name','is_hot','is_new']