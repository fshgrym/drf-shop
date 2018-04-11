#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# Author:fsh
#time:'2018/3/10 23:17:31下午'

#独立使用django model

import sys
import os

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd+'../')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MxShop.settings")

import django
django.setup()
#以上写好就能直接使用django model 独立出来使用

from goods.models import Goods,GoodsCategory,GoodsImage

from db_tools.data.product_data import row_data

for goods_derail in row_data:
    goods=Goods()
    goods.name = goods_derail['name']
    goods.market_price = float(int(goods_derail['market_price'].replace('￥','').replace('元','')))
    goods.shop_price = float(int(goods_derail['sale_price'].replace('￥','').replace('元','')))
    goods.goods_brief = goods_derail['desc'] if goods_derail['desc'] is not None else ''
    goods.goods_front_image = goods_derail['images'][0] if goods_derail['images'] else ''


    category_name = goods_derail['categorys'][-1]
    category = GoodsCategory.objects.filter(name=category_name)
    if category:
        goods.category = category[0]
    goods.save()

    for goods_image in goods_derail['images']:
        goods_image_instance = GoodsImage()
        goods_image_instance.image = goods_image
        goods_image_instance.goods = goods
        goods_image_instance.save()


