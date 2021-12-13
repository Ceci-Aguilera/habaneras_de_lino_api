from django.contrib import admin
from django.conf.urls import url,include
from .views import *

app_name = 'store_admin_app'

urlpatterns = [
	url(r'^index/$',IndexView ,name='index-view'),
	url(r'^login/$',LoginView ,name='login-view'),
	url(r'^logout/$',LogoutView ,name='logout-view'),
	url(r'^categories/$',CategoriesView ,name='categories-view'),
	url(r'^collections/$',CollectionsView ,name='collections-view'),
	url(r'^orders/$',OrdersView ,name='orders-view'),
	url(r'^products/$',ProductsView ,name='products-view'),
	url(r'^custom-colors/$',CustomColorsView ,name='custom-colors-view'),
	url(r'^category/create/$',CreateCategoryView ,name='category-create-view'),
	url(r'^collection/create/$',CreateCollectionView ,name='collection-create-view'),
	url(r'^product/create/$',CreateProductView ,name='product-create-view'),
	url(r'^custom-colors/create/$',CreateCustomColorsView ,name='custom-colors-create-view'),
	url(r'^category/crud/(?P<id>[0-9]+)/$',CategoryCRUDView ,name='category-crud-view'),
	url(r'^collection/crud/(?P<id>[0-9]+)/$',CollectionCRUDView ,name='collection-crud-view'),
	url(r'^order/(?P<id>[0-9]+)/$',OrderDetailView ,name='order-detail-view'),
	url(r'^product/crud/(?P<id>[0-9]+)/$',ProductCRUDView ,name='product-crud-view'),
	url(r'^custom-colors/crud/(?P<id>[0-9]+)/$',CustomColorsCRUDView ,name='custom-colors-crud-view'),
]
