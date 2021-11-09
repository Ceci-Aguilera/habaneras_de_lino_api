from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.conf import settings
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

import json
from datetime import datetime
from random import randint

from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import *
from rest_framework.views import APIView

from .models import *
from .serializers import *

from store_app.models import *

def IndexView(request):
	if request.user is None or request.user.is_authenticated == False:
		return redirect('/store-admin/login/')
	return render(request, "store_admin_app/index.html",{})

#=============================================================================

def LoginView(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/store-admin/index/')
	elif request.method == 'GET':
		if request.user is not None and request.user.is_authenticated == True:
			return HttpResponseRedirect('/store-admin/index/')
		else:
			return render(request, "store_admin_app/login.html",{})
	return render(request, "store_admin_app/login.html",{})

#=============================================================================

def LogoutView(request):
	logout(request)
	return HttpResponseRedirect('/store-admin/index/')

#=============================================================================

def CategoriesView(request):
	if request.user is None or request.user.is_authenticated == False:
		return redirect('/store-admin/login/')

	if request.method == "GET":
		categories = Category.objects.all()
		return render(request, "store_admin_app/categories.html",{"categories":categories})

	elif request.method == 'POST':
		query = request.POST['search_category']
		categories = Category.objects.filter(title__icontains=query)
		return render(request, "store_admin_app/categories.html",{"categories":categories})


#=============================================================================

def ProductsView(request):
	if request.user is None or request.user.is_authenticated == False:
		return redirect('/store-admin/login/')

	if request.method == "GET":
		products = Product.objects.all()
		return render(request, "store_admin_app/products.html",{"products":products})

	elif request.method == 'POST':
		query = request.POST['search_product']
		products = Product.objects.filter(title__icontains=query)
		return render(request, "store_admin_app/products.html",{"products":products})

#=============================================================================

def CreateCategoryView(request):
	if request.user is None or request.user.is_authenticated == False:
		return redirect('/store-admin/login/')

	if request.method == "GET":
		return render(request, "store_admin_app/category_create.html",{})

	elif request.method == 'POST':
		try:
			title = request.POST['title']
			image = request.FILES['image']
			category = Category.objects.create(title=title, image = image)
		except:
			pass
		return redirect('/store-admin/categories/')

#=============================================================================

def CreateProductView(request):
	if request.user is None or request.user.is_authenticated == False:
		return redirect('/store-admin/login/')

	if request.method == "GET":
		categories = Category.objects.all()
		return render(request, "store_admin_app/product_create.html",{"categories":categories})

	elif request.method == 'POST':
		try:
			title = request.POST['title']
			price = request.POST['price']
			subtag = request.POST['subtag']
			category = Category.objects.get(title = request.POST['category'])
			image = request.FILES['image']
			product = Product.objects.create(title=title, image = image, price=price, subtag=subtag, category=category)
		except:
			pass
		return redirect('/store-admin/products/')

def CategoryCRUDView(request, id):
	if request.user is None or request.user.is_authenticated == False:
		return redirect('/store-admin/login/')

	if request.method == "GET":
		category = Category.objects.get(id=id)
		category_image = str(category.image.url)
		return render(request, "store_admin_app/category_crud.html",{"category":category, "category_image":category_image})

	elif request.method == 'POST':
		try:
			title = request.POST['title']
			image = request.FILES['image']
			category = Category.objects.get(id=id)
			category.title = title
			category.image = image
			category.save()
		except:
			title = request.POST['title']
			category = Category.objects.get(id=id)
			Category.objects.get(id=id)
			category.title = title
			category.save()
		return redirect('/store-admin/categories/')
