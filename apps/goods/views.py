from django.shortcuts import render

# Create your views here.
'''
继承关系
1、GenericViewSet(viewset) -drf
    2、GenericView         -drf
         3、APIView        -drf
              4、View      -django
mixin(通过mixin来区别)
    CreateModelMixin   #新建创建
    ListModelMixin     #列表全部
    RetrieveModelMixin #获取详情
    UpdateModelMixin   #更新和部分修改
    DestroyModelMixin  #删除功能
'''
from .serializers import GoodsSerializer,IndexCategorySerializer,CategorySerializer,BannerSerializer
from rest_framework.views import APIView
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle
from rest_framework.response import Response
from rest_framework import generics, mixins,filters
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets #比较重要的view，后面会经常使用，尽量使用这个
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from django_filters.rest_framework import DjangoFilterBackend
from .models import Banner,Goods,GoodsCategory
from .filters import ProductFilter
class GoodsResultsSetPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100


class GoodsListViewSet(CacheResponseMixin,mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    """
    list:
        商品列表页
    retrieve:
        商品详情页
    """

    # GenericAPIView 一个很重要的View,对APIView进行再次封装
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsResultsSetPagination
    throttle_classes = (UserRateThrottle,AnonRateThrottle)
    #过滤
    # filter_backends = (DjangoFilterBackend,)
    # filter_fields = ('name', 'shop_price')

    filter_class = ProductFilter

    filter_backends = (filters.SearchFilter,DjangoFilterBackend,filters.OrderingFilter)
    search_fields = ('name', 'goods_brief','goods_desc')# = 精确搜索 ^开头必须是
    """
    '^'开始 - 搜索。
    '='完全匹配。
    '@'全文搜索。（目前只支持Django的MySQL后端。）
    '$'正则表达式搜索
    """
    ordering_fields = ('sold_num', 'shop_price')
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num +=1 #浏览+1
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    # def get_queryset(self):
    #     '''
    #     重载了就不需要queryset = Goods.objects.all()
    #     :return:
    #     '''
    #     queryset = Goods.objects.all()
    #     price_min = self.request.query_params.get('price_min',0)
    #     if price_min :
    #         queryset.objects.filter(shop_price__gt=int(price_min))
    #     return queryset
# class GoodsListView(generics.ListAPIView):
#     """
#     商品列表页
#     """
#     # GenericAPIView 一个很重要的View,对APIView进行再次封装
#     queryset = Goods.objects.all()
#     serializer_class = GoodsSerializer
#     pagination_class = GoodsResultsSetPagination
#     # 分页在setting配置
#
#
#     # def get(self, request, *args, **kwargs):
#     #     return self.list(request, *args, **kwargs)

# class GoodsListView(APIView):
#     """
#     List all goods
#     """
#
#     def get(self, request, format=None):
#         goods = Goods.objects.all()[:10]
#         goods_serializer = GoodsSerializer(goods, many=True)  # many序列化成数组对象
#         return Response(goods_serializer.data)
#
#     # def post(self, request, format=None):
#     #     serializer = GoodsSerializer(data=request.data)#django没有request.data,而rest进行封装，取用户发过来的post，body的数据
#     #     if serializer.is_valid():
#     #         serializer.save()#serializer会去调用GoodsSerializer的create方法
#     #         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    """
    list:
        商品分类列表数量
    retrieve:
        获取商品详情

    """

    queryset =  GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer
class BannerViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
    '''
    获取轮播图列表
    '''
    queryset = Banner.objects.all().order_by('index')
    serializer_class = BannerSerializer
class IndexCategoryViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
    '''
    首页商品分类
    '''
    queryset = GoodsCategory.objects.filter(is_tab=True,name__in=('生鲜食品','酒水饮料'))
    serializer_class = IndexCategorySerializer

