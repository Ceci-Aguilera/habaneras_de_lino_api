from django.contrib import admin
from django.conf.urls import url,include
from .views import *

app_name = 'store_app'

urlpatterns = [
	url(r'^categories/$',CategoryListView.as_view(),name='category-list-view'),
	url(r'^categories/men/$',CategoryMenListView.as_view(),name='category-list-men-view'),
	url(r'^categories/woman$',CategoryWomenListView.as_view(),name='category-list-women-view'),
	url(r'^collections/$',CustomCollectionListView.as_view(),name='collection-list-view'),
	url(r'^collections/men/$',CustomCollectionMenListView.as_view(),name='collection-list-men-view'),
	url(r'^collections/women/$',CustomCollectionWomenListView.as_view(),name='collection-list-woman-view'),
	url(r'^collection/title/(?P<title>[\w\-]+)/$',CustomCollectionTitleDetailView.as_view(),name='collection-title-view'),
	url(r'^products-extra-tags/$',ProductsPerExtraTag.as_view(),name='products-extra-tags-list-view'),
	url(r'^collections/(?P<id>[0-9]+)/$',CustomCollectionDetailView.as_view(),name='collection-list-view'),
	url(r'^product-images/(?P<id>[0-9]+)/$', ProductImagesView.as_view(), name='product-images-detail-api'),
	url(r'^categories/(?P<id>[0-9]+)/$', CategoryDetailView.as_view(), name='category-detail-api'),
	url(r'^products/$',ProductListView.as_view(),name='products-list-view'),
	url(r'^products/(?P<id>[0-9]+)/$', ProductDetailView.as_view(), name='products-detail-api'),
	url(r'^cart/(?P<token>[0-9A-Za-z_\-]+)/$',CartView.as_view(),name='cart-detail-view'),
	url(r'^cart/$',CartView.as_view(),name='cart-view'),
	url(r'^cart/delete-product/(?P<id>[0-9]+)/$', ProductVariationView.as_view(), name='delete-product-api'),
	url(r'^custom-products/$',ProductVariationListView.as_view(),name='custom-products-list-view'),
	url(r'^custom-products/(?P<id>[0-9]+)/$', ProductVariationView.as_view(), name='custom-products-detail-api'),
	url(r'^order/(?P<cart_token>[0-9A-Za-z_\-]+)/$', CheckoutView.as_view(), name='checkout-detail-api'),
]
