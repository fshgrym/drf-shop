"""Mx URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.views.generic import TemplateView
from django.conf.urls import url, include
from django.views.static import serve
import xadmin
from rest_framework.documentation import include_docs_urls
from MxShop.settings import MEDIA_ROOT
from goods.views import GoodsListViewSet, CategoryViewSet,BannerViewSet,IndexCategoryViewSet
from users.views import SmsCodeViewSet, UserViewSet
from user_operation.views import UserFavViewSet,LeavingMessingViewSet,AddressViewSet
from trade.views import ShoppingCatViewSet,OrderViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token
from trade.views import AliPayView
# goods_list = GoodsListViewSet.as_view({
#     'get': 'list',#绑定get方法
#     # 'post': 'create'
# })
router = DefaultRouter()
# 配置goods的url
router.register(r'goods', GoodsListViewSet, base_name='goods')#商品
router.register(r'categorys', CategoryViewSet, base_name='categorys')#类别
router.register(r'codes', SmsCodeViewSet, base_name='codes')#验证码
router.register(r'users', UserViewSet, base_name='users')#用户信息
router.register(r'userfavs', UserFavViewSet, base_name='userfavs')#用户收藏
router.register(r'messages',LeavingMessingViewSet,base_name='messages')#用户消息
router.register(r'address',AddressViewSet,base_name='address')#用户收货信息
router.register(r'shopcarts',ShoppingCatViewSet,base_name='shopcarts')#购物车
router.register(r'orders',OrderViewSet,base_name='orders')
router.register(r'banners',BannerViewSet,base_name='banners')#轮播图
router.register(r'indexgoods',IndexCategoryViewSet,base_name='indexgoods')#主页商品系列
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^xadmin/', xadmin.site.urls),
    url(r'media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    url(r'^index/',TemplateView.as_view(template_name='index.html'),name='index'),
    # 商品列表
    # url(r'goods/$',GoodsListView.as_view(),name='goods-list'),
    # url(r'goods/$',goods_list,name='goods-list'),
    url(r'docs/', include_docs_urls(title='幕学生鲜')),  # 文档
    url(r'^api-auth/', include('rest_framework.urls')),  # 登录
    url(r'^api-token-auth/', views.obtain_auth_token),  # drf认证接口
    url(r'^login/$', obtain_jwt_token),  # jwt验证登录 接口
    url(r'^alipay/return/',AliPayView.as_view(),name='alipay'),#支付宝接口
    url('', include('social_django.urls', namespace='social'))#第三方登录

]
