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
from django.db.models import Q

import json
from datetime import datetime
from random import randint

from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import *
from rest_framework.views import APIView

from .models import *
from .serializers import *

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

from store_app.models import *

def IndexView(request):
	if request.user is None or request.user.is_authenticated == False:
		return redirect('/store-admin/login/')

	top_amount = min(len(Product.objects.all()),10)
	top_ten = Product.objects.all().order_by('-amount_sold')[:2]

	top_products = Product.objects.all().order_by('-amount_sold')
	return render(request, "store_admin_app/index.html",{'top_ten_products': top_ten, "top_products": top_products})

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

def CollectionsView(request):
	if request.user is None or request.user.is_authenticated == False:
		return redirect('/store-admin/login/')

	if request.method == "GET":
		collections = CustomCollection.objects.all()
		return render(request, "store_admin_app/collections.html",{"collections":collections})

	elif request.method == 'POST':
		query = request.POST['search_collection']
		collections = CustomCollection.objects.filter(title__icontains=query)
		return render(request, "store_admin_app/collections.html",{"collections":collections})


#=============================================================================

def ProductsView(request):
	if request.user is None or request.user.is_authenticated == False:
		return redirect('/store-admin/login/')

	if request.method == "GET":
		collections = CustomCollection.objects.all()
		products = Product.objects.all()
		return render(request, "store_admin_app/products.html",{"products":products,"collections":collections, "default_collection":"All"})

	elif request.method == 'POST':
		collections = CustomCollection.objects.all()

		if 'search_product' in request.POST:
			default_collection = "All"
			query = request.POST['search_product']
			products = Product.objects.filter(title__icontains=query)
		else:
			query = request.POST['filter_collection']
			if query == 'All':
				default_collection = "All"
				products = Product.objects.all()
			else:
				default_collection = query
				products = Product.objects.filter(collection__title=query)

		return render(request, "store_admin_app/products.html",{"products":products,"collections":collections, "default_collection": default_collection})


#=============================================================================

def OrdersView(request):
	if request.user is None or request.user.is_authenticated == False:
		return redirect('/store-admin/login/')

	status_map = {"Ordered": "Pedido por cliente", "OrderedMex": "Pedido a Mexico",
				  "ProdMex": "Produciendose en Mexico",
				  "ToUSA": "Camino a USA", "ToUPS": "En USA Listo para UPS", "UPS": "UPS: Camino a cliente",
				  "Received": "Recibido por cliente", "Canceled": "Cancelada", "Refund": "Refund"}

	if request.method == "GET":

		orders = Order.objects.all().filter(payment__isnull=False)
		return render(request, "store_admin_app/orders.html",{"orders":orders, "status_map": status_map, "default_order_status": "All"})

	elif request.method == 'POST':
		if 'search_order' in request.POST:
			default_order_status = "All"
			query = request.POST['search_order']
			orders = Order.objects.filter(Q(user_first_name__icontains=query) | Q(user_last_name__icontains=query) | Q(email__icontains=query)).filter(payment__isnull=False)
		else:
			query = request.POST['filter_order_status']
			default_order_status = query
			if query == 'All':
				orders = Order.objects.all().filter(payment__isnull=False)
			else:
				orders = Order.objects.filter(status=query).filter(payment__isnull=False)
		return render(request, "store_admin_app/orders.html",{"orders":orders, "status_map": status_map, "default_order_status": default_order_status})




def CustomColorsView(request):
	if request.user is None or request.user.is_authenticated == False:
		return redirect('/store-admin/login/')

	if request.method == "GET":
		available_colors = CustomColor.objects.all()
		return render(request, "store_admin_app/available_colors.html",{"available_colors":available_colors})

	elif request.method == 'POST':
		query = request.POST['search_available_colors']
		available_colors = CustomColor.objects.filter(title__icontains=query)
		return render(request, "store_admin_app/available_colors.html",{"available_colors":available_colors})











#=============================================================================

def OrderDetailView(request, id):
	if request.user is None or request.user.is_authenticated == False:
		return redirect('/store-admin/login/')

	if request.method == "GET":
		order = Order.objects.get(id=id)
		payment = Payment.objects.get(id = order.payment.id)

		status_map = {"Ordered": "Pedido por cliente", "OrderedMex": "Pedido a Mexico",
					  "ProdMex": "Produciendose en Mexico",
					  "ToUSA": "Camino a USA", "ToUPS": "En USA Listo para UPS", "UPS": "UPS: Camino a cliente",
					  "Received": "Recibido por cliente", "Canceled": "Cancelada", "Refund": "Refund"}

		products = order.cart.product_variation_set.all()

		return render(request, "store_admin_app/order_detail.html",{"order": order, "status_map": status_map, "payment": payment, "cart": order.cart, "products": products})

	if request.method == "POST":

		order = Order.objects.get(id=id)
		payment = Payment.objects.get(id=order.payment.id)

		products = order.cart.product_variation_set.all()

		status_map = {"Ordered": "Pedido por cliente", "OrderedMex": "Pedido a Mexico", "ProdMex": "Produciendose en Mexico",
					  "ToUSA": "Camino a USA", "ToUPS": "En USA Listo para UPS", "UPS": "UPS: Camino a cliente",
					  "Received": "Recibido por cliente", "Canceled": "Cancelada", "Refund": "Refund"}

		if 'save' in request.POST:
			order_status = request.POST['order_status']
			order.status = order_status
			order.save()


		elif 'refund' in request.POST:
			client_id = payment.stripe_charge_id

			try:
				result_refund = stripe.Refund.create(
					charge=client_id,
				)

				if(result_refund.status == "succeeded"):
					payment.refund = "Refund successfully made"
				else:
					payment.refund = "Error"
				payment.save()
			except:
				payment.refund = "Error"
				payment.save()

		return render(request, "store_admin_app/order_detail.html", {"order": order, "status_map": status_map, "payment": payment, "cart": order.cart, "products": products})

















#=============================================================================

def CreateCategoryView(request):
	if request.user is None or request.user.is_authenticated == False:
		return redirect('/store-admin/login/')

	if request.method == "GET":
		return render(request, "store_admin_app/category_create.html",{"message": "No Error"})

	elif request.method == 'POST':
		try:
			title = request.POST['title']
			if title.isspace() or (not title):
				return render(request, "store_admin_app/category_create.html",
							  {"message": "Introduzca el titulo de la categoria"})
			else:
				if 'image' in request.FILES:
					image = request.FILES['image']
					Category.objects.create(title=title, image = image)
					return redirect('/store-admin/categories/')
				else:
					return render(request, "store_admin_app/category_create.html",{"message": "Introduzca la foto de la categoria"})
		except:
			return render(request, "store_admin_app/category_create.html",{"message": "Error"})



#=============================================================================

def CreateCollectionView(request):
	if request.user is None or request.user.is_authenticated == False:
		return redirect('/store-admin/login/')

	if request.method == "GET":
		return render(request, "store_admin_app/collection_create.html",{"message": "No Error"})

	elif request.method == 'POST':
		try:
			title = request.POST['title']
			if title.isspace() or (not title):
				return render(request, "store_admin_app/collection_create.html",
						  {"message": "Introduzca el titulo de la coleccion"})
			if 'image' in request.FILES:
				description = request.POST['description']
				image = request.FILES['image']
				CustomCollection.objects.create(title=title, description=description, image=image)
				return redirect('/store-admin/collections/')
			else:
				return render(request, "store_admin_app/collection_create.html",
							  {"message": "Introduzca la foto de la coleccion"})
		except:
			pass
		return redirect('/store-admin/collections/')



#=============================================================================
def CreateCustomColorsView(request):
	if request.user is None or request.user.is_authenticated == False:
		return redirect('/store-admin/login/')

	if request.method == "GET":
		return render(request, "store_admin_app/available_colors_create.html", {"message": "No Error"})

	elif request.method == 'POST':
		try:
			title = request.POST['title']
			if title.isspace() or (not title):
				return render(request, "store_admin_app/available_colors_create.html",
							  {"message": "Introduzca el titulo del color personalizado"})

			code = request.POST['code']

			CustomColor.objects.create(title=title, code=code)
		except:
			print(code)
			return render(request, "store_admin_app/available_colors_create.html",
						  {"message": "Error"})
		return redirect('/store-admin/custom-colors/')





#=============================================================================

def CreateProductView(request):
	if request.user is None or request.user.is_authenticated == False:
		return redirect('/store-admin/login/')

	if request.method == "GET":
		categories = Category.objects.all()
		available_colors = CustomColor.objects.all()
		collections = CustomCollection.objects.all()
		return render(request, "store_admin_app/product_create.html",
					  {"categories":categories, "available_colors": available_colors,
					   "collections": collections,
					   "messages": []})

	elif request.method == 'POST':

		categories = Category.objects.all()
		available_colors = CustomColor.objects.all()
		collections = CustomCollection.objects.all()


		try:
			messages = []
			title = request.POST['title']
			if title.isspace() or (not title):
				messages.append("Introduzca el titulo del producto")

			code = request.POST['code']
			if code.isspace() or (not code):
				messages.append("Introduzca el codigo del producto")

			price = request.POST['price']
			if price.isspace() or (not price):
				messages.append("Introduzca el precio del producto")

			subtag = request.POST['subtag']

			if (not 'category' in request.POST) or (not request.POST['category']) or request.POST['category'].isspace():
				messages.append("Introduzca la categoria del producto")
			else:
				print("Not Ok")
				category = Category.objects.get(title = request.POST['category'])

			if 'image' in request.FILES:
				image = request.FILES['image']
			else:
				messages.append("Introduzca la foto del producto")

			if 's_image' in request.FILES:
				s_image = request.FILES['s_image']
			else:
				messages.append("Introduzca la foto secundaria del producto")

			extra_tag = request.POST['extra_tag']
			description = request.POST['description']

			if messages == []:
				product = Product.objects.create(title=title, code=code, image=image, s_image=s_image, price=price, subtag=subtag,
												 category=category, extra_tag=extra_tag, description=description)
				ProductImage.objects.create(product=product, image=product.image, type='first')
				ProductImage.objects.create(product=product, image=product.s_image, type='second')

			else:
				return render(request, "store_admin_app/product_create.html",
					  {"categories":categories, "available_colors": available_colors,
					   "collections": collections,
					   "messages": messages})


		except:
			return render(request, "store_admin_app/product_create.html",
						  {"categories": categories, "available_colors": available_colors,
						   "collections": collections,
						   "messages": ("Error")})

		# Check Available Colors
		try:
			a_colors = request.POST.getlist('a_colors')

			for prod_col in a_colors:
				prod_col = CustomColor.objects.get(title=prod_col)
				product.available_colors.add(prod_col)
		except:
			pass

		# Check collections
		try:
			new_collections = request.POST.getlist('new_collections')

			for prod_coll in new_collections:
				prod_coll = CustomCollection.objects.get(title=prod_coll)
				product.collection.add(prod_coll)
		except:
			pass

		# Check for new Extra Images
		if (len(request.FILES.getlist('extra_images')) > 0):
			new_extra_imgs = request.FILES.getlist('extra_images')

			for new_extra_img in new_extra_imgs:
				ProductImage.objects.create(product=product, image=new_extra_img, type='extra')

		else:
			pass

		product.save()

		return redirect('/store-admin/products/')


















# ======================================================================================================================
#	CRUD Category
# ======================================================================================================================
def CategoryCRUDView(request, id):
	if request.user is None or request.user.is_authenticated == False:
		return redirect('/store-admin/login/')

	if request.method == "GET":
		category = Category.objects.get(id=id)
		category_image = str(category.image.url)
		return render(request, "store_admin_app/category_crud.html",{"category":category, "category_image":category_image,
																	 "message": "No Error"})

	elif request.method == 'POST':
		if "save" in request.POST:
			try:
				category = Category.objects.get(id=id)
				category_image = str(category.image.url)
				title = request.POST['title']

				if title.isspace() or (not title):
					return render(request, "store_admin_app/category_crud.html",
								  {"category": category, "category_image": category_image,
								   "message": "Introduzca el titulo de la categoria"})
				else:
					if 'image' in request.FILES:
						image = request.FILES['image']
						category.title = title
						category.image = image
						category.save()
					else:
						category.title = title
						category.save()
						return redirect('/store-admin/categories/')
			except:
				pass
		else:
			category = Category.objects.get(id=id)
			category.delete()

		return redirect('/store-admin/categories/')




# ======================================================================================================================
#	CRUD Collection
# ======================================================================================================================
def CollectionCRUDView(request, id):
	if request.user is None or request.user.is_authenticated == False:
		return redirect('/store-admin/login/')

	if request.method == "GET":
		collection = CustomCollection.objects.get(id=id)
		if collection.image==None or not collection.image:
			image = None
		else:
			image = str(collection.image.url)
		return render(request, "store_admin_app/collection_crud.html",{"collection":collection,
																	   "image":image,
																	   "message": "No Error"})

	elif request.method == 'POST':

		if "save" in request.POST:

			collection = CustomCollection.objects.get(id=id)
			coll_image = str(collection.image.url)

			try:
				title = request.POST['title']
				if title.isspace() or (not title):
					return render(request, "store_admin_app/collection_crud.html",
								  {"collection": collection, "image": coll_image,
								   "message": "Introduzca el titulo de la coleccion"})

				if 'image' in request.FILES:
					image = request.FILES['image']
					collection.image = image
				description = request.POST['description']
				collection.title = title
				collection.description = description
				collection.save()
			except:
				pass
		else:
			collection = CustomCollection.objects.get(id=id)
			collection.delete()

		return redirect('/store-admin/collections/')






# ======================================================================================================================
#	CRUD Custom Colors
# ======================================================================================================================
def CustomColorsCRUDView(request, id):
	if request.user is None or request.user.is_authenticated == False:
		return redirect('/store-admin/login/')

	if request.method == "GET":
		custom_color = CustomColor.objects.get(id=id)
		return render(request, "store_admin_app/available_colors_crud.html",{"custom_color":custom_color,
																			 "message": "No Error"})

	elif request.method == 'POST':
		custom_color = CustomColor.objects.get(id=id)

		if "save" in request.POST:
			try:
				title = request.POST['title']
				if title.isspace() or (not title):
					return render(request, "store_admin_app/available_colors_crud.html",
								  {"custom_color": custom_color,
								   "message": "Introduzca el titulo del color personalizado"})
				code = request.POST['code']
				custom_color.title = title
				custom_color.code = code
				custom_color.save()
			except:
				return render(request, "store_admin_app/available_colors_crud.html",
							  {"custom_color": custom_color,
							   "message": "Error"})
		else:
			custom_color.delete()

		return redirect('/store-admin/custom-colors/')



# ======================================================================================================================
#	CRUD Product
# ======================================================================================================================
def ProductCRUDView(request, id):
	if request.user is None or request.user.is_authenticated == False:
		return redirect('/store-admin/login/')

	if request.method == "GET":
		product = Product.objects.get(id=id)
		product_image = str(product.image.url)
		if product.s_image==None or not product.s_image:
			product_s_image = None
		else:
			product_s_image = str(product.s_image.url)
		categories = Category.objects.all()
		available_colors = CustomColor.objects.all()
		product_colors = product.available_colors.all()
		collections = CustomCollection.objects.all()
		product_collections = product.collection.all()
		extra_images = ProductImage.objects.filter(product=product, type='extra')

		return render(request, "store_admin_app/product_crud.html", {
			"product": product,
			"product_image": product_image,
			"product_s_image": product_s_image,
			"categories": categories,
			"available_colors": available_colors,
			"product_colors": product_colors,
			"collections": collections,
			"product_collections": product_collections,
			"extra_images": extra_images,
			"messages": []
			}
		)

	elif request.method == 'POST':


		product = Product.objects.get(id=id)

		if "save" in request.POST:

			product_image = str(product.image.url)
			product_s_image = str(product.s_image.url)
			categories = Category.objects.all()
			available_colors = CustomColor.objects.all()
			product_colors = product.available_colors.all()
			collections = CustomCollection.objects.all()
			product_collections = product.collection.all()
			extra_images = ProductImage.objects.filter(product=product, type='extra')

			messages = []




			title = request.POST['title']
			if title.isspace() or (not title):
				messages.append("Introduzca el titulo del producto")

			code = request.POST['code']
			if code.isspace() or (not code):
				messages.append("Introduzca el codigo del producto")

			price = request.POST['price']
			if price.isspace() or (not price):
				messages.append("Introduzca el precio del producto")


			if (messages != []):
				return render(request, "store_admin_app/product_crud.html", {
					"product": product,
					"product_image": product_image,
					"product_s_image": product_s_image,
					"categories": categories,
					"available_colors": available_colors,
					"product_colors": product_colors,
					"collections": collections,
					"product_collections": product_collections,
					"extra_images": extra_images,
					"messages": messages
				}
				)


			category = request.POST['category']
			category = Category.objects.get(title = category)
			subtag = request.POST['subtag']
			extra_tag = request.POST['extra_tag']
			description = request.POST['description']



			# Check if images were updated
			try:
				new_image = request.FILES['image']
				product.image = new_image
				product.save()
				ProductImage.objects.get(product__id=product.id, type='first').delete()
				ProductImage.objects.create(product=product, image=product.image, type='first')
			except:
				pass

			try:
				new_s_image = request.FILES['product_s_image']
				product.s_image = new_s_image
				product.save()
				ProductImage.objects.get(product__id=product.id, type='second').delete()

				ProductImage.objects.create(product=product, image=product.s_image, type='second')
			except:
				pass

			# Check for new Extra Images
			if(len(request.FILES.getlist('extra_images')) > 0):
				new_extra_imgs = request.FILES.getlist('extra_images')

				old_extra_images = ProductImage.objects.filter(product=product, type='extra')

				for old_extra_img in old_extra_images:
					old_extra_img.delete()
				for new_extra_img in new_extra_imgs:
					ProductImage.objects.create(product=product, image=new_extra_img, type='extra')

			else:
				pass


			# Check available colors
			try:
				a_colors = request.POST.getlist('a_colors')
				product_colors = product.available_colors.all()

				for prod_col in product_colors:
					product.available_colors.remove(prod_col)

				for prod_col in a_colors:
					prod_col = CustomColor.objects.get(title = prod_col)
					product.available_colors.add(prod_col)
			except:
				pass

			# Check collections
			try:
				new_collections = request.POST.getlist('new_collections')
				product_collections = product.collection.all()

				for prod_coll in product_collections:
					product.collection.remove(prod_coll)

				for prod_coll in new_collections:
					prod_coll = CustomCollection.objects.get(title=prod_coll)
					product.collection.add(prod_coll)
			except:
				pass


			product.title = title
			product.code = code
			product.price = price
			product.category = category
			product.subtag = subtag
			product.extra_tag = extra_tag
			product.description = description
			product.save()

		else:
			product.delete()

		return redirect('/store-admin/products/')




def CuponsListView(request):
	if request.user is None or request.user.is_authenticated == False:
		return redirect('/store-admin/login/')

	if request.method == "GET":
		coupons = Coupon.objects.all()
		return render(request, "store_admin_app/coupons.html", {"coupons": coupons})

	elif request.method == 'POST':
		query = request.POST['search_coupon']
		coupons = Coupon.objects.filter(user_email__icontains=query)
		return render(request, "store_admin_app/coupons.html", {"coupons": coupons})




def CuponsCreatelView(request):
	if request.user is None or request.user.is_authenticated == False:
		return redirect('/store-admin/login/')

	if request.method == "GET":
		return render(request, "store_admin_app/coupon_create.html", {"message": "No Error"})

	elif request.method == 'POST':
		try:
			user_email = request.POST['user_email']
			if user_email.isspace() or (not user_email):
				return render(request, "store_admin_app/coupon_create.html",
							  {"message": "Introduzca el email del usuario"})

			code = request.POST['code']
			if code.isspace() or (not code):
				return render(request, "store_admin_app/coupon_create.html",
							  {"message": "Introduzca el codigo del cupon"})

			discount_type = request.POST['discount_type']

			discount = request.POST['discount']
			if discount.isspace() or (not discount):
				return render(request, "store_admin_app/coupon_create.html",
							  {"message": "Introduzca el descuento del cupon"})

			how_many_items = request.POST['how_many_items']
			if how_many_items.isspace() or (not how_many_items):
				return render(request, "store_admin_app/coupon_create.html",
							  {"message": "Introduzca la cantidad de productos"})


			Coupon.objects.create(user_email = user_email, code = code, discount=discount, discount_type = discount_type, how_many_items = how_many_items, cart=None, taken=False)
			return redirect('/store-admin/coupons/')
		except:
			pass
		return redirect('/store-admin/coupons/')



def CuponCRUDView(request, id):
	if request.user is None or request.user.is_authenticated == False:
		return redirect('/store-admin/login/')

	if request.method == "GET":
		coupon = Coupon.objects.get(id=id)
		return render(request, "store_admin_app/coupon_crud.html",{"coupon":coupon,
																			 "message": "No Error"})

	elif request.method == 'POST':
		coupon = Coupon.objects.get(id=id)

		if "save" in request.POST:
			try:
				user_email = request.POST['user_email']
				if user_email.isspace() or (not user_email):
					return render(request, "store_admin_app/coupon_crud.html",
								  {"coupon": coupon,
								   "message": "Introduzca el email del cliente"})

				code = request.POST['code']
				if code.isspace() or (not code):
					return render(request, "store_admin_app/coupon_crud.html",
								  {"coupon": coupon,
								   "message": "Introduzca el codigo del cupon"})

				discount = request.POST['discount']
				if discount.isspace() or (not discount):
					return render(request, "store_admin_app/coupon_crud.html",
								  {"coupon": coupon,
								   "message": "Introduzca el descuento del cupon"})

				how_many_items = request.POST['how_many_items']
				if how_many_items.isspace() or (not how_many_items):
					return render(request, "store_admin_app/coupon_crud.html",
								  {"coupon": coupon,
								   "message": "Introduzca la cantidad de productos"})

				discount_type = request.POST['discount_type']

				coupon.user_email = user_email
				coupon.code = code
				coupon.discount = discount
				coupon.how_many_items = how_many_items
				coupon.discount_type = discount_type

				coupon.save()
			except:
				return render(request, "store_admin_app/coupon_crud.html",
							  {"coupon": coupon,
							   "message": "Error"})
		else:
			coupon.delete()

		return redirect('/store-admin/coupons/')