#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# Author:fsh
# time:'2018/3/12 23:00:01下午'
# import json
#
# from django.views.generic.base import View  # 最底层的view
#
# from goods.models import Goods


# class GoodsList(View):
#     def get(self, request):
#         '''
#         通过django的view实现商品列表页
#         :param request:
#         :return:
#         '''
#         goods = Goods.objects.all()[:10]
#         json_list = []
#         # for good in goods:
#         #     json_dict = {}
#         #     json_dict['name'] = good.name
#         #     json_dict['category'] = good.category.name
#         #     json_dict['market_price'] = good.market_price
#         #     json_list.append(json_dict)
#
#
#         from django.forms.models import model_to_dict
#         # for good in goods:
#         #     json_dict = model_to_dict(good)
#         #     json_list.append(json_dict)
#
#
#         from django.core import serializers #专门用来序列化的
#         json_data = serializers.serialize('json',goods)
#         json_data = json.loads(json_data)
#
#
#         from django.http import HttpResponse ,JsonResponse
#         # return HttpResponse(json_data, content_type='application/json')
#         return JsonResponse(json_data,safe=False)
from urllib import request
proxy = request.ProxyHandler({'http':'58.19.12.103:18118'})
opener = request.build_opener(proxy)
opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.3 Safari/537.36')]
request.install_opener(opener)
res = request.urlopen('http://www.ip138.com/').read().decode('gb2312')
print(res)
