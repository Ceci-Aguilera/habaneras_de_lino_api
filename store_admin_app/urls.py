from django.contrib import admin
from django.conf.urls import url,include
from .views import *

app_name = 'store_admin_app'

urlpatterns = [
	url(r'^index/$',IndexView ,name='index-view'),
	url(r'^login/$',LoginView ,name='login-view'),
	url(r'^logout/$',LogoutView ,name='logout-view'),
	url(r'^categories/$',CategoriesView ,name='categories-view'),
]
