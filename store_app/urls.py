from django.contrib import admin
from django.conf.urls import url,include
from .views import *

app_name = 'store_app'

urlpatterns = [
	url(r'^categories/$',CategoryListView.as_view(),name='category-list-view'),
	url(r'^categories/(?P<id>[0-9]+)/$', CategoryDetailView.as_view(), name='category-detail-api'),
	url(r'^products/$',ProductListView.as_view(),name='products-list-view'),
	url(r'^products/(?P<id>[0-9]+)/$', ProductDetailView.as_view(), name='products-detail-api'),
	url(r'^cart/$',CartView.as_view(),name='cart-view'),
]
